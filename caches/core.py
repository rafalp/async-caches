from typing import Any, Union
from urllib.parse import SplitResult, parse_qsl, urlsplit

from .types import Serializable, Version


class Cache:
    SUPPORTED_BACKENDS = {
        "dummy": "caches.backends.dummy:DummyBackend",
        "locmem": "caches.backends.locmem:LocMemBackend",
        "redis": "caches.backends.redis:RedisBackend",
    }

    def __init__(self, url: Union[str, "CacheURL"], *, prefix: str = ""):
        self.url = CacheURL(url)

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