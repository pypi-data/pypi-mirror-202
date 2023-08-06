from abc import abstractmethod, ABC
from contextlib import asynccontextmanager


class BaseRoomCommands(ABC):
    @abstractmethod
    async def get(self, id_: str) -> str: ...

    @abstractmethod
    async def find(self, type_: str) -> str | None: ...

    @abstractmethod
    async def delete(self, id_: str): ...

    @abstractmethod
    async def save(self, id_: str, json_data: str): ...

    @asynccontextmanager
    async def lock(self, id_: str): ...
