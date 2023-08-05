from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import Protocol


class BaseRoomCommands(Protocol):
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
