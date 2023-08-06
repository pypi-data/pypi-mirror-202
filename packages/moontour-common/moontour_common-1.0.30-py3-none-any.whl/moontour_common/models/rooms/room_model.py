import uuid
from datetime import datetime
from enum import StrEnum
from typing import Generic, TypeVar

from pydantic import Field, validator
from pydantic.generics import GenericModel

from moontour_common.models.rooms.participants.participant import Participant
from moontour_common.models.rooms.phase import Phase


class RoomStatus(StrEnum):
    waiting = 'waiting'
    waiting_to_start = 'waitingToStart'
    running = 'running'
    closed = 'closed'


PhaseType = TypeVar('PhaseType', bound=Phase)
ParticipantType = TypeVar('ParticipantType', bound=Participant)
ParticipantState = TypeVar('ParticipantState', bound=Participant)


class RoomModel(GenericModel, Generic[PhaseType, ParticipantType, ParticipantState]):
    id: str = Field(alias='id_', default_factory=lambda: str(uuid.uuid4()))
    type: str = None
    map: str = 'world'
    status: RoomStatus = RoomStatus.waiting
    create_time: datetime = Field(default_factory=datetime.now)
    phases: list[PhaseType] = []
    participants_data: dict[str, tuple[ParticipantType, ParticipantState]]

    @property
    def participants(self) -> dict[str, ParticipantType]:
        return {key: participant for key, (participant, _) in self.participants_data.items()}

    @property
    def participants_state(self) -> dict[str, ParticipantState]:
        return {key: state for key, (_, state) in self.participants_data.items()}

    def is_full(self):
        return all([participant.is_full() for participant in self.participants.values()])

    @validator("type", always=True)
    def compute_type(cls, _):
        return cls.__name__

    class Config:
        allow_population_by_field_name = True
