from .base import BaseBackend


class LocMemBackend(BaseBackend):
    _caches = {}

    async def connect(self):
        return True

    async def disconnect(self):
        return True

    async def get(
        self, key: str, default: Any, *, version: Optional[Version] = None
    ) -> Any:
        raise NotImplementedError()

    async def set(
        self, key: str, value: Serializable, *, version: Optional[Version] = None
    ) -> Any:
        raise NotImplementedError()
