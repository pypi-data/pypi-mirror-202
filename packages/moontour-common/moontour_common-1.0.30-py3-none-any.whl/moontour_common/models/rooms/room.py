from abc import ABC
from collections.abc import Awaitable
from contextlib import asynccontextmanager
from typing import TypeVar, Callable, ParamSpec, Generic, ClassVar

from aio_pika import Message

from moontour_common.commands.base_room_commands import BaseRoomCommands
from moontour_common.commands.redis_room_commands import RedisRoomCommands
from moontour_common.database.rabbitmq import get_rooms_exchange
from moontour_common.models.coordinates import Coordinates
from moontour_common.models.guess import Guess
from moontour_common.models.rooms.phase import PhaseStatus
from moontour_common.models.rooms.room_model import RoomModel, RoomStatus, PhaseType, ParticipantType, ParticipantState
from moontour_common.models.user import User

RoomType = TypeVar('RoomType', bound='Room')

P = ParamSpec('P')
T = TypeVar('T')


def modify_room(func: Callable[P, T]) -> Callable[P, Awaitable[T]]:
    async def wrapper(*args, **kwargs):
        room: 'Room' = args[0]
        async with room.modify():
            return func(*args, **kwargs)

    return wrapper


class Room(RoomModel[PhaseType, ParticipantType, ParticipantState], ABC,
           Generic[PhaseType, ParticipantType, ParticipantState]):
    commands: ClassVar[BaseRoomCommands] = RedisRoomCommands()

    @classmethod
    async def get(cls: type[RoomType], id_: str) -> RoomType:
        room_raw = await Room.commands.get(id_)
        return cls.parse_raw(room_raw)

    @classmethod
    async def find(cls: type[RoomType]) -> RoomType | None:
        room_raw = await Room.commands.find(cls.__name__)
        if room_raw is not None:
            return cls.parse_raw(room_raw)

    @staticmethod
    async def delete(id_: str):
        await Room.commands.delete(id_)

    async def reload(self):
        new_room = await self.get(self.id)
        self.__dict__.update(new_room.__dict__)

    async def save(self):
        await self.commands.save(self.id, self.json())

    async def notify(self):
        exchange = await get_rooms_exchange()
        await exchange.publish(
            message=Message(body=self.json().encode()),
            routing_key=f'{self.id}.*',
        )

    @asynccontextmanager
    async def modify(self):
        async with self.commands.lock(self.id):
            await self.reload()
            try:
                yield
            except Exception:
                raise
            else:
                await self.save()
                await self.notify()

    def _get_participant(self, user_id: str) -> ParticipantType | None:
        for participant in self.participants.values():
            if user_id in participant.get_user_ids():
                return participant

    @modify_room
    def join(self, user: User):
        if self.status != RoomStatus.waiting:
            return
        for participant in self.participants.values():
            if not participant.is_full():
                participant.insert_user(user)
                break
        if all([participant.is_full() for participant in self.participants.values()]):
            self.status = RoomStatus.waiting_to_start

    @modify_room
    def leave(self, user_id: str):
        for participant in self.participants.values():
            participant.remove_user(user_id)

    @modify_room
    def start(self):
        self.status = RoomStatus.running

    @modify_room
    def add_phase(self, phase: PhaseType):
        self.phases.append(phase)

    @modify_room
    def start_phase(self):
        self.phases[-1].status = PhaseStatus.running

    @modify_room
    def guess(self, user_id: str, coordinates: Coordinates):
        phase = self.phases[-1]
        if self.status == RoomStatus.running and phase.status == PhaseStatus.running:
            guess = Guess(coordinates=coordinates)
            phase.insert_guess(user_id, guess)
            self._on_guess(user_id, guess)

    def _on_guess(self, user_id: str, guess: Guess):
        pass

    @modify_room
    def finish_phase(self):
        phase = self.phases[-1]
        phase.status = PhaseStatus.finished
        self._finalize_phase(phase)

    def _finalize_phase(self, phase: PhaseType):
        pass

    @modify_room
    def close(self):
        self.status = RoomStatus.closed
