import asyncio
import json
from inspect import isawaitable
from typing import Any, Dict, Iterable, Mapping, Optional, Union

import aioredis

from ..types import Serializable
from ..core import CacheURL
from .base import BaseBackend


class RedisBackend(BaseBackend):
    _pool: aioredis.RedisConnection

    def __init__(self, cache_url: Union[CacheURL, str], **options: Any) -> None:
        self._cache_url = CacheURL(cache_url)
        self._options = options
        self._pool = None

    def _get_connection_kwargs(self) -> dict:
        url_options = self._cache_url.options

        kwargs = {}
        minsize = url_options.get("minsize")
        maxsize = url_options.get("maxsize")

        if minsize is not None:
            kwargs["minsize"] = int(minsize)
        if maxsize is not None:
            kwargs["maxsize"] = int(maxsize)

        if self._options.get("minsize") is not None:
            kwargs["minsize"] = int(self._options["minsize"])
        if self._options.get("maxsize") is not None:
            kwargs["maxsize"] = int(self._options["maxsize"])

        return kwargs

    async def connect(self):
        # pylint: disable=attribute-defined-outside-init
        assert self._pool is None, "Cache backend is already running"
        kwargs = self._get_connection_kwargs()
        self._pool = await aioredis.create_pool(str(self._cache_url), **kwargs)

    async def disconnect(self):
        assert self._pool is not None, "Cache backend is not running"
        self._pool.close()
        await self._pool.wait_closed()

    async def get(self, key: str, default: Any) -> Any:
        value = await self._pool.execute("GET", key)
        return json.loads(value) if value is not None else default

    async def set(
        self, key: str, value: Serializable, *, timeout: Optional[int]
    ) -> Any:
        if timeout is None:
            await self._pool.execute("SET", key, json.dumps(value))
        elif timeout:
            await self._pool.execute("SETEX", key, timeout, json.dumps(value))

    async def add(self, key: str, value: Serializable, *, timeout: Optional[int]):
        if timeout is None:
            await self._pool.execute("SET", key, json.dumps(value), "NX")
        elif timeout:
            await self._pool.execute("SET", key, json.dumps(value), "EX", timeout, "NX")

    async def get_or_set(
        self, key: str, default: Any, *, timeout: Optional[int]
    ) -> Any:
        value = await self.get(key, None)
        if value is None:
            if callable(default):
                default = default()
                if isawaitable(default):
                    default = await default
            await self.set(key, default, timeout=timeout)
            return default
        return value

    async def get_many(self, keys: Iterable[str]) -> Dict[str, Any]:
        values = await self._pool.execute("MGET", *keys)
        return {
            key: json.loads(values[i]) if values[i] is not None else None
            for i, key in enumerate(keys)
        }

    async def set_many(
        self, mapping: Mapping[str, Serializable], *, timeout: Optional[int]
    ):
        if timeout is None or timeout:
            values = []
            for key, value in mapping.items():
                values.append(key)
                values.append(json.dumps(value))
            await self._pool.execute("MSET", *values)
        if timeout:
            expire = []
            for key in mapping:
                expire.append(self._pool.execute("EXPIRE", key, timeout))
            await asyncio.gather(*expire)

    async def delete(self, key: str):
        await self._pool.execute("UNLINK", key)

    async def delete_many(self, keys: Iterable[str]):
        await self._pool.execute("UNLINK", *keys)

    async def clear(self):
        await self._pool.execute("FLUSHDB", "async")

    async def touch(self, key: str, timeout: Optional[int]) -> bool:
        if timeout is None:
            return bool(await self._pool.execute("PERSIST", key))
        if timeout:
            return bool(await self._pool.execute("EXPIRE", key, timeout))
        return bool(await self._pool.execute("UNLINK", key))

    async def incr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        if not await self._pool.execute("EXISTS", key):
            raise ValueError(f"'{key}' is not set in the cache")
        if isinstance(delta, int):
            return await self._pool.execute("INCRBY", key, delta)
        if isinstance(delta, float):
            return json.loads(await self._pool.execute("INCRBYFLOAT", key, delta))
        raise ValueError(f"incr value must be int or float")

    async def decr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        if not await self._pool.execute("EXISTS", key):
            raise ValueError(f"'{key}' is not set in the cache")
        if isinstance(delta, int):
            return await self._pool.execute("INCRBY", key, delta * -1)
        if isinstance(delta, float):
            return json.loads(
                await self._pool.execute("INCRBYFLOAT", key, delta * -1.0)
            )
        raise ValueError(f"decr value must be int or float")
