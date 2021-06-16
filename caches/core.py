import json
from types import TracebackType
from typing import Any, Awaitable, Coroutine, Dict, Iterable, Mapping, Optional, Type, Union
from urllib.parse import SplitResult, parse_qsl, urlsplit

from .importer import import_from_string
from .types import Serializable, Version


class Cache:
    SUPPORTED_BACKENDS = {
        "dummy": "caches.backends.dummy:DummyBackend",
        "locmem": "caches.backends.locmem:LocMemBackend",
        "redis": "caches.backends.redis:RedisBackend",
        "rediss": "caches.backends.redis:RedisBackend",
    }

    def __init__(
        self,
        url: Union[str, "CacheURL"],
        *,
        ttl: Optional[int] = None,
        version: Optional[Version] = None,
        key_prefix: str = "",
        **options: Any,
    ):
        self.url = CacheURL(url)

        url_options = self.url.options
        self.ttl = ttl
        self.version = version or url_options.get("version", "")
        self.key_prefix = key_prefix or url_options.get("key_prefix", "")

        if self.ttl is None and url_options.get("ttl") is not None:
            self.ttl = int(url_options["ttl"])

        if ttl == 0 or self.ttl == 0:
            raise ValueError(
                "'ttl' option can't be set to 0. "
                "If you want cache keys to never expire, set it to 'None'."
            )

        self.options = options
        self.is_connected = False

        assert self.url.backend in self.SUPPORTED_BACKENDS, f"Invalid backend {self.url.backend}."
        backend_str = self.SUPPORTED_BACKENDS[self.url.backend]
        backend_cls = import_from_string(backend_str)

        from .backends.base import BaseBackend

        assert issubclass(backend_cls, BaseBackend)
        self._backend = backend_cls(
            self.url,
            ttl=self.ttl,
            version=self.version,
            key_prefix=self.key_prefix,
            **options,
        )

    async def connect(self) -> None:
        assert not self.is_connected, "Already connected."
        await self._backend.connect()
        self.is_connected = True

    async def disconnect(self) -> None:
        assert self.is_connected, "Already disconnected."
        await self._backend.disconnect()
        self.is_connected = False

    async def __call__(self, coroutine: Coroutine, ttl: Optional[int] = None) -> Any:
        """Cached coroutine call by itself.

        Example:
            >>> async def my_coroutine(*args, **kwargs):
            >>>   pass
            >>>
            >>> async with Cache("locmem://") as cache:
            >>>   await cache(my_coroutine('arg', test1='kwarg')

        Args:
            coroutine (Coroutine): Coroutine that you can cache
            ttl (int): TTL of the cached value

        Returns:
            Any: Return value of the coroutine.
        """
        key = await self._get_key_from_coroutine(coroutine)

        return await self.get_or_set(key, coroutine, ttl=ttl)

    async def __aenter__(self) -> "Cache":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        await self.disconnect()

    def make_key(self, key: str, version: Optional[Version] = None) -> str:
        return "%s:%s:%s" % (self.key_prefix, version or self.version, key)

    def make_ttl(self, ttl: Optional[int] = None) -> Optional[int]:
        if ttl == 0:
            raise ValueError(
                "'ttl' can't be set to 0. "
                "If you want cache to never expire, set it to 'None'."
            )
        if ttl is not None:
            return ttl
        if self.ttl is not None:
            return self.ttl
        return None

    async def get(
        self, key: str, default: Any = None, *, version: Optional[Version] = None
    ) -> Any:
        """Gets key value from cache, or default if key was not found or expired."""
        key_ = self.make_key(key, version)
        return await self._backend.get(key_, default)

    async def set(
        self,
        key: str,
        value: Serializable,
        *,
        ttl: Optional[int] = None,
        version: Optional[Version] = None,
    ) -> Any:
        """Sets value for key in cache."""
        key_ = self.make_key(key, version)
        ttl_ = self.make_ttl(ttl)
        await self._backend.set(key_, value, ttl=ttl_)

    async def add(
        self,
        key: str,
        value: Serializable,
        *,
        ttl: Optional[int] = None,
        version: Optional[Version] = None,
    ) -> bool:
        """Sets value for key in cache, but only if key wasn't already set."""
        key_ = self.make_key(key, version)
        ttl_ = self.make_ttl(ttl)
        return await self._backend.add(key_, value, ttl=ttl_)

    async def get_or_set(
        self,
        key: str,
        default: Union[Awaitable[Serializable], Serializable],
        *,
        ttl: Optional[int] = None,
        version: Optional[Version] = None,
    ) -> Any:
        """Gets key value from cache, or default if key was not found or expired.
        If key was not found in the cache, it will be set with default value."""
        key_ = self.make_key(key, version)
        ttl_ = self.make_ttl(ttl)
        return await self._backend.get_or_set(key_, default, ttl=ttl_)

    async def get_many(
        self, keys: Iterable[str], version: Optional[Version] = None
    ) -> Dict[str, Any]:
        """Gets values for specified keys from cache. If key didn't exist or was
        expired, its value will be None."""
        keys_ = {key: self.make_key(key, version) for key in keys}
        values = await self._backend.get_many(list(keys_.values()))
        return {key: values[keys_[key]] for key in keys}

    async def set_many(
        self, mapping: Mapping[str, Serializable], *, ttl: Optional[int] = None
    ):
        """Sets values for specified keys in cache."""
        mapping_ = {self.make_key(key): mapping[key] for key in mapping}
        ttl_ = self.make_ttl(ttl)
        await self._backend.set_many(mapping_, ttl=ttl_)

    async def delete(self, key: str, version: Optional[Version] = None):
        """Deletes specified key from cache."""
        key_ = self.make_key(key, version)
        await self._backend.delete(key_)

    async def delete_many(self, keys: Iterable[str], version: Optional[Version] = None):
        """Deletes specified keys from cache."""
        keys_ = [self.make_key(key, version) for key in keys]
        await self._backend.delete_many(keys_)

    async def clear(self):
        """Deletes all keys from cache."""
        await self._backend.clear()

    async def touch(
        self, key: str, ttl: Optional[int] = None, *, version: Optional[Version] = None
    ) -> bool:
        """Updates key's expiration time in cache."""
        key_ = self.make_key(key, version)
        ttl_ = self.make_ttl(ttl)
        return await self._backend.touch(key_, ttl_)

    async def incr(
        self,
        key: str,
        delta: Union[float, int] = 1,
        *,
        version: Optional[Version] = None,
    ) -> Union[float, int]:
        """Increases key value in cache by delta. Defaults to '1'."""
        key_ = self.make_key(key, version)
        return await self._backend.incr(key_, delta)

    async def decr(
        self,
        key: str,
        delta: Union[float, int] = 1,
        *,
        version: Optional[Version] = None,
    ) -> Union[float, int]:
        """Decreases key value in cache by delta. Defaults to '1'."""
        key_ = self.make_key(key, version)
        return await self._backend.decr(key_, delta)

    async def _get_key_from_coroutine(self, coroutine: Coroutine) -> str:
        """Gets key from coroutine name and its arguments.

        Args:
            coroutine (Coroutine)

        Returns:
            str: Key in string.
        """
        frame = coroutine.cr_frame

        coroutine_name = coroutine.__qualname__
        coroutine_arguments = frame.f_locals

        args = [arg for arg in coroutine_arguments.get('args', [])]
        kwargs = coroutine_arguments.get('kwds')

        return self.make_key(json.dumps([coroutine_name, args, kwargs]))


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

    @property
    def options(self) -> dict:
        if not hasattr(self, "_options"):
            # pylint: disable=attribute-defined-outside-init
            self._options = dict(parse_qsl(self.components.query))
        return self._options

    def __str__(self) -> str:
        return self._url

    def __repr__(self) -> str:
        url = str(self)
        return f"{self.__class__.__name__}({repr(url)})"

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)
