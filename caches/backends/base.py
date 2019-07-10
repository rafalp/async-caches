from typing import Any, Optional

from ..types import Serializable, Version


class BaseBackend:
    async def connect(self):
        raise NotImplementedError()

    async def disconnect(self):
        raise NotImplementedError()

    def make_key(self, key: str, version: Optional[Version] = None) -> str:
        pass

    async def get(
        self, key: str, default: Any, *, version: Optional[Version] = None
    ) -> Any:
        raise NotImplementedError()

    async def set(
        self, key: str, value: Serializable, *, version: Optional[Version] = None
    ) -> Any:
        raise NotImplementedError()
