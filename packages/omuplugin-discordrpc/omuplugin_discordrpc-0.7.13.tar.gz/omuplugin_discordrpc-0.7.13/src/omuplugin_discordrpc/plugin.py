from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field

from loguru import logger
from omu.omu import Omu

from .const import PLUGIN_APP, PORT_MAX, PORT_MIN
from .discordrpc import DiscordRPC
from .discordrpc.payloads import (
    AuthenticateUser,
    GetChannelsResponseData,
    GetGuildsResponseData,
    SpeakingStartData,
    SpeakingStopData,
    VoiceStateItem,
)
from .types import (
    GET_CHANNELS_ENDPOINT_TYPE,
    GET_CLIENTS_ENDPOINT_TYPE,
    GET_GUILDS_ENDPOINT_TYPE,
    REFRESH_ENDPOINT_TYPE,
    SESSION_REGISTRY_TYPE,
    SET_VC_ENDPOINT_TYPE,
    SPEAKING_STATE_REGISTRY_TYPE,
    VOICE_STATE_REGISTRY_TYPE,
    WAIT_FOR_READY_ENDPOINT_TYPE,
    GetChannelsRequest,
    GetGuildsRequest,
    SetVCRequest,
    SpeakState,
)

omu = Omu(PLUGIN_APP)
voice_state_registry = omu.registries.get(VOICE_STATE_REGISTRY_TYPE)
speaking_state_registry = omu.registries.get(SPEAKING_STATE_REGISTRY_TYPE)
session_registry = omu.registries.get(SESSION_REGISTRY_TYPE)


@dataclass
class Client:
    port: int
    rpc: DiscordRPC
    user: AuthenticateUser
    access_token: str
    closed: bool = False
    vc_rpc: DiscordRPC | None = None
    channel_id: str | None = None
    vc_states: dict[str, VoiceStateItem] = field(default_factory=dict)
    speaking_states: dict[str, SpeakState] = field(default_factory=dict)

    @classmethod
    async def try_connect(cls, port: int) -> Client:
        sessions = await session_registry.get()
        exist_session = sessions["sessions"].get(port, None)
        if exist_session:
            try:
                rpc = await DiscordRPC.connect(port)
                authenticate_res = await rpc.authenticate(exist_session["access_token"])
                return cls(
                    port,
                    rpc,
                    authenticate_res["user"],
                    exist_session["access_token"],
                )
            except Exception as e:
                logger.warning(f"Failed to connect to {port}: {e}")
                sessions["sessions"].pop(port)
                await session_registry.set(sessions)
        rpc = await DiscordRPC.connect(port)
        authorize_res = await rpc.authorize(["rpc", "messages.read"])
        access_token = await rpc.fetch_access_token(authorize_res["code"])
        sessions["sessions"][port] = {"access_token": access_token}
        await session_registry.set(sessions)
        authenticate_res = await rpc.authenticate(access_token)
        return cls(
            port,
            rpc,
            authenticate_res["user"],
            access_token,
        )

    async def get_guilds(self) -> GetGuildsResponseData:
        return await self.rpc.get_guilds()

    async def get_channels(self, guild_id: str) -> GetChannelsResponseData:
        return await self.rpc.get_channels(guild_id)

    async def connect_vc(self, channel_id: str):
        self.channel_id = channel_id
        if self.vc_rpc is not None:
            await self.vc_rpc.close()
        self.vc_rpc = await DiscordRPC.connect(self.port)
        await self.vc_rpc.authenticate(self.access_token)
        vc_states: dict[str, VoiceStateItem] = {}
        speaking_states: dict[str, SpeakState] = {}
        await voice_state_registry.set(vc_states)
        await speaking_state_registry.set(speaking_states)

        async def voice_state_create(data: VoiceStateItem):
            vc_states[data["user"]["id"]] = data
            await voice_state_registry.set(vc_states)

        async def voice_state_update(data: VoiceStateItem):
            vc_states[data["user"]["id"]] = data
            await voice_state_registry.set(vc_states)

        async def voice_state_delete(data: VoiceStateItem):
            vc_states.pop(data["user"]["id"], None)
            await voice_state_registry.set(vc_states)

        await self.vc_rpc.subscribe_voice_state_create(channel_id, voice_state_create)
        await self.vc_rpc.subscribe_voice_state_update(channel_id, voice_state_update)
        await self.vc_rpc.subscribe_voice_state_delete(channel_id, voice_state_delete)

        async def speaking_start_handler(data: SpeakingStartData):
            existing = speaking_states.get(data["user_id"], {})
            speaking_states[data["user_id"]] = {
                "speaking": True,
                "speaking_start": int(time.time() * 1000),
                "speaking_stop": existing.get("speaking_stop", 0),
            }
            await speaking_state_registry.set(speaking_states)

        await self.vc_rpc.subscribe_speaking_start(channel_id, speaking_start_handler)

        async def speaking_stop_handler(data: SpeakingStopData):
            existing = speaking_states.get(data["user_id"], {})
            speaking_states[data["user_id"]] = {
                "speaking": False,
                "speaking_start": existing.get("speaking_start", 0),
                "speaking_stop": int(time.time() * 1000),
            }
            await speaking_state_registry.set(speaking_states)

        await self.vc_rpc.subscribe_speaking_stop(channel_id, speaking_stop_handler)

    async def close_vc(self):
        if self.vc_rpc is not None:
            await self.vc_rpc.close()
            self.vc_rpc = None

    async def close(self):
        await self.rpc.close()
        if self.vc_rpc is not None:
            await self.vc_rpc.close()


clients: dict[str, Client] = {}
current_client: Client | None = None


@omu.endpoints.bind(endpoint_type=GET_CLIENTS_ENDPOINT_TYPE)
async def get_clients(_: None) -> dict[str, AuthenticateUser]:
    return {port: client.user for port, client in clients.items()}


@omu.endpoints.bind(endpoint_type=GET_GUILDS_ENDPOINT_TYPE)
async def get_guilds(req: GetGuildsRequest) -> GetGuildsResponseData:
    user_id = req["user_id"]
    if user_id not in clients:
        raise Exception(f"User {user_id} not found. {clients.keys()}")
    client = clients[user_id]
    return await client.get_guilds()


@omu.endpoints.bind(endpoint_type=GET_CHANNELS_ENDPOINT_TYPE)
async def get_channels(req: GetChannelsRequest) -> GetChannelsResponseData:
    user_id = req["user_id"]
    if user_id not in clients:
        raise Exception(f"User {user_id} not found. {clients.keys()}")
    client = clients[user_id]
    return await client.get_channels(req["guild_id"])


@omu.endpoints.bind(endpoint_type=SET_VC_ENDPOINT_TYPE)
async def set_vc(req: SetVCRequest) -> None:
    global current_client
    if current_client is not None and current_client.channel_id == req["channel_id"]:
        return None
    user_id = req["user_id"]
    if user_id not in clients:
        raise Exception(f"User {user_id} not found. {clients.keys()}")
    client = clients[user_id]
    if current_client is not None:
        await current_client.close_vc()
    current_client = client
    await client.connect_vc(req["channel_id"])
    return None


refresh_task: asyncio.Task | None = None


@omu.endpoints.bind(endpoint_type=WAIT_FOR_READY_ENDPOINT_TYPE)
async def wait_for_vc(_: None) -> None:
    if refresh_task is None:
        return
    await refresh_task


async def refresh_clients():
    for client in clients.values():
        if client.closed:
            await client.close()

    async def connect_client(port: int):
        try:
            client = await Client.try_connect(port)
            clients[client.user["id"]] = client
            logger.info(f"Connected to {port}")
        except Exception as e:
            logger.warning(f"Failed to connect to {port}: {e}")

    tasks = [connect_client(port) for port in range(PORT_MIN, PORT_MAX)]
    await asyncio.gather(*tasks)

    session = await session_registry.get()
    user_id = session["user_id"]
    channel_id = session["channel_id"]
    if user_id is None or channel_id is None:
        return
    if user_id not in clients:
        return
    client = clients[user_id]
    await client.connect_vc(channel_id)


@omu.endpoints.bind(endpoint_type=REFRESH_ENDPOINT_TYPE)
async def refresh(_: None) -> None:
    await refresh_clients()
    return None


@omu.on_ready
async def on_ready():
    global refresh_task
    await voice_state_registry.set({})
    await speaking_state_registry.set({})
    refresh_task = asyncio.create_task(refresh_clients())
