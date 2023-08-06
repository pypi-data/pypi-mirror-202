from abc import ABC, abstractmethod
from random import randint

from pydantic import Field, BaseModel
from pydantic.color import Color

from moontour_common.models.user import User


def get_random_color() -> Color:
    def get_component() -> int:
        return randint(0, 255)

    return Color((get_component(), get_component(), get_component()))


class Participant(BaseModel, ABC):
    color: Color = Field(default_factory=get_random_color)

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
