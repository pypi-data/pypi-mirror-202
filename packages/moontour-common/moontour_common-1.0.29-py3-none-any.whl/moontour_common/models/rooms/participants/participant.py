from abc import ABC, abstractmethod
from random import randint
from typing import TypeVar, Generic

from pydantic import Field
from pydantic.color import Color
from pydantic.generics import GenericModel

from moontour_common.models.user import User


def get_random_color() -> Color:
    def get_component() -> int:
        return randint(0, 255)

    return Color((get_component(), get_component(), get_component()))


ParticipantState = TypeVar('ParticipantState')


class Participant(GenericModel, Generic[ParticipantState], ABC):
    color: Color = Field(default_factory=get_random_color)
    state: ParticipantState

    def __init__(self, **kwargs):
        state_type: type[ParticipantState] = self.__fields__['state'].type_
        super().__init__(state=state_type(), **kwargs)

    @abstractmethod
    def insert_user(self, user: User):
        raise NotImplementedError()

    @abstractmethod
    def remove_user(self, user_id: str):
        raise NotImplementedError()

    @abstractmethod
    def is_full(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_user_ids(self) -> set[str]:
        raise NotImplementedError()
