from typing import Protocol


class FileStorage(Protocol):

    async def save(self, data: bytes, extension: str, ) -> str:
        pass