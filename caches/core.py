from typing import Any, Optional, Union
from urllib.parse import SplitResult, urlsplit

from .types import Serializable, Version


class Cache:
    SUPPORTED_BACKENDS = {
        "dummy": "caches.backends.dummy:DummyBackend",
        "locmem": "caches.backends.locmem:LocMemBackend",
        "redis": "caches.backends.redis:RedisBackend",
    }

    def __init__(self, url: Union[str, "CacheURL"], *, prefix: str = ""):
        self.url = CacheURL(url)
        self.prefix = prefix
        self.is_connected = False

        assert self.url.backend in self.SUPPORTED_BACKENDS, "Invalid backend."
        backend_str = self.SUPPORTED_BACKENDS[self.url.backend]

    async def connect(self) -> None:
        assert not self.is_connected, "Already connected."
        await self._backend.connect()
        self.is_connected = True

    async def disconnect(self) -> None:
        assert self.is_connected, "Already disconnected."
        await self._backend.disconnect()
        self.is_connected = False

    async def get(
        self, key: str, default: Any, *, version: Optional[Version] = None
    ) -> Any:
        raise NotImplementedError()

    async def set(
        self, key: str, value: Serializable, *, version: Optional[Version] = None
    ) -> Any:
        raise NotImplementedError()


class CacheURL:
    def __init__(self, url: Union[str, "DatabaseURL"]):
        self._url = str(url)

    @property
    def components(self) -> SplitResult:
        if not hasattr(self, "_components"):
            self._components = urlsplit(self._url)
        return self._components

    @property
    def backend(self) -> str:
        return self.components.scheme

    @property
    def hostname(self) -> Optional[str]:
        return self.components.hostname

    @property
    def port(self) -> Optional[int]:
        return self.components.port

    @property
    def netloc(self) -> Optional[str]:
        return self.components.netloc or None

    @property
    def database(self) -> str:
        path = self.components.path
        if path.startswith("/"):
            path = path[1:]
        return path or None

    def __str__(self) -> str:
        return self._url

    def __repr__(self) -> str:
        url = str(self)
        return f"{self.__class__.__name__}({repr(url)})"

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)
