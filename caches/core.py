from time import time
from typing import Any, Dict, Iterable, Mapping, Optional, Union
from urllib.parse import SplitResult, urlsplit

from .importer import import_from_string
from .types import Serializable, Version


class Cache:
    SUPPORTED_BACKENDS = {
        "dummy": "caches.backends.dummy:DummyBackend",
        "locmem": "caches.backends.locmem:LocMemBackend",
        "redis": "caches.backends.redis:RedisBackend",
    }

    def __init__(
        self,
        url: Union[str, "CacheURL"],
        *,
        timeout: Optional[int] = None,
        version: Optional[Version] = None,
        key_prefix: str = "",
    ):
        self.url = CacheURL(url)
        self.timeout = timeout
        self.version = version or ""
        self.key_prefix = key_prefix
        self.is_connected = False

        assert self.url.backend in self.SUPPORTED_BACKENDS, "Invalid backend."
        backend_str = self.SUPPORTED_BACKENDS[self.url.backend]
        backend_cls = import_from_string(backend_str)

        from .backends.base import BaseBackend

        assert issubclass(backend_cls, BaseBackend)
        self._backend = backend_cls(
            self.url,
            timeout=self.timeout,
            version=self.version,
            key_prefix=self.key_prefix,
        )

    async def connect(self) -> None:
        assert not self.is_connected, "Already connected."
        await self._backend.connect()
        self.is_connected = True

    async def disconnect(self) -> None:
        assert self.is_connected, "Already disconnected."
        await self._backend.disconnect()
        self.is_connected = False

    def make_key(self, key: str, version: Optional[Version] = None) -> str:
        return "%s:%s:%s" % (self.key_prefix, version or self.version, key)

    def make_timeout(self, timeout: Optional[int] = None) -> Optional[int]:
        if timeout is not None:
            return int(time()) + timeout
        if self.timeout is not None:
            return int(time()) + self.timeout
        return None

    async def get(
        self, key: str, default: Any = None, *, version: Optional[Version] = None
    ) -> Any:
        key_ = self.make_key(key, version)
        return await self._backend.get(key_, default)

    async def set(
        self,
        key: str,
        value: Serializable,
        *,
        timeout: Optional[int] = None,
        version: Optional[Version] = None,
    ) -> Any:
        key_ = self.make_key(key, version)
        timeout_ = self.make_timeout(timeout)
        await self._backend.set(key_, value, timeout=timeout_)

    async def add(
        self,
        key: str,
        value: Serializable,
        *,
        timeout: Optional[int] = None,
        version: Optional[Version] = None,
    ):
        key_ = self.make_key(key, version)
        timeout_ = self.make_timeout(timeout)
        await self._backend.add(key_, value, timeout=timeout_)

    async def get_or_set(
        self,
        key: str,
        default: Any,
        *,
        timeout: Optional[int] = None,
        version: Optional[Version] = None,
    ) -> Any:
        key_ = self.make_key(key, version)
        timeout_ = self.make_timeout(timeout)
        return await self._backend.get_or_set(key_, default, timeout=timeout_)

    async def get_many(
        self, keys: Iterable[str], version: Optional[Version] = None
    ) -> Dict[str, Any]:
        keys_ = {key: self.make_key(key, version) for key in keys}
        values = await self._backend.get_many(list(keys_.values()))
        return {key: values[keys_[key]] for key in keys}

    async def set_many(
        self, mapping: Mapping[str, Serializable], *, timeout: Optional[int] = None
    ):
        mapping_ = {self.make_key(key): mapping[key] for key in mapping}
        timeout_ = self.make_timeout(timeout)
        await self._backend.set_many(mapping_, timeout=timeout_)

    async def delete(self, key: str, version: Optional[Version] = None):
        key_ = self.make_key(key, version)
        await self._backend.delete(key_)

    async def delete_many(self, keys: Iterable[str], version: Optional[Version] = None):
        keys_ = [self.make_key(key, version) for key in keys]
        await self._backend.delete_many(keys_)

    async def clear(self):
        await self._backend.clear()

    async def touch(
        self,
        key: str,
        timeout: Optional[int] = None,
        *,
        version: Optional[Version] = None,
    ) -> bool:
        key_ = self.make_key(key, version)
        timeout_ = self.make_timeout(timeout)
        return await self._backend.touch(key_, timeout_)

    async def incr(
        self,
        key: str,
        delta: Union[float, int] = 1,
        *,
        version: Optional[Version] = None,
    ) -> Union[float, int]:
        key_ = self.make_key(key, version)
        return await self._backend.incr(key_, delta)

    async def decr(
        self,
        key: str,
        delta: Union[float, int] = 1,
        *,
        version: Optional[Version] = None,
    ) -> Union[float, int]:
        key_ = self.make_key(key, version)
        return await self._backend.decr(key_, delta)


class CacheURL:
    def __init__(self, url: Union[str, "CacheURL"]):
        self._url = str(url)

    @property
    def components(self) -> SplitResult:
        if not hasattr(self, "_components"):
            # pylint: disable=attribute-defined-outside-init
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
    def database(self) -> Optional[str]:
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
