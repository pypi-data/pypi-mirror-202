from contextlib import asynccontextmanager
from datetime import timedelta

from redis.commands.json.path import Path
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import ResponseError

from moontour_common.commands.base_room_commands import BaseRoomCommands
from moontour_common.database.redis import redis_client
from moontour_common.models.rooms.room import RoomStatus

KEY_PREFIX = 'room:'
ROOMS_INDEX = 'rooms_idx'


def get_room_key(id_: str) -> str:
    return f'{KEY_PREFIX}{id_}'


class RedisRoomCommands(BaseRoomCommands):
    def __init__(self):
        """
        FT.CREATE rooms_idx ON JSON PREFIX 1 room: SCHEMA
            $.type AS type TEXT
            $.status AS status TEXT
        """
        try:
            await redis_client.ft(ROOMS_INDEX).info()
        except ResponseError:
            schema = [TextField("$.type", as_name="type"), TextField("$.status", as_name="status")]
            await redis_client.ft(ROOMS_INDEX).create_index(
                schema,
                definition=IndexDefinition(prefix=[KEY_PREFIX], index_type=IndexType.JSON)
            )
            await redis_client.expire(KEY_PREFIX, timedelta(days=1))

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
