from contextlib import asynccontextmanager

from redis.commands.json.path import Path

from moontour_common.commands.base_room_commands import BaseRoomCommands
from moontour_common.database.redis import redis_client
from moontour_common.models.rooms.room_model import RoomStatus

KEY_PREFIX = 'room:'
ROOMS_INDEX = 'rooms_idx'


def get_room_key(id_: str) -> str:
    return f'{KEY_PREFIX}{id_}'


class RedisRoomCommands(BaseRoomCommands):
    async def get(self, id_: str) -> str:
        return await redis_client.execute_command('JSON.GET', get_room_key(id_), Path.root_path())

    async def find(self, type_: str) -> str | None:
        result = await redis_client.ft(ROOMS_INDEX).search(
            f'@type:{type_} @status:{RoomStatus.waiting}')

        if len(result.docs) > 0:
            return result.docs[0].json

    async def delete(self, id_: str):
        await redis_client.execute_command('JSON.DEL', get_room_key(id_), Path.root_path())

    async def save(self, id_: str, json_data: str):
        await redis_client.execute_command('JSON.SET', get_room_key(id_), Path.root_path(), json_data)

    @asynccontextmanager
    async def lock(self, id_: str):
        async with redis_client.lock(f'room-{id_}'):
            yield
