import asyncio
import json
from typing import Any, Dict, Iterable, Mapping, Optional, Union

import aioredis

from ..types import Serializable
from .base import BaseBackend


class RedisBackend(BaseBackend):
    async def connect(self):
        # pylint: disable=attribute-defined-outside-init
        self._pool = await aioredis.create_pool(
            str(self._cache_url), minsize=5, maxsize=10, loop=asyncio.get_event_loop()
        )

    async def disconnect(self):
        self._pool.close()
        await self._pool.wait_closed()

    async def get(self, key: str, default: Any) -> Any:
        value = await self._pool.execute("get", key)
        return json.loads(value) if value is not None else default

    async def set(
        self, key: str, value: Serializable, *, timeout: Optional[int]
    ) -> Any:
        if timeout is None:
            await self._pool.execute("set", key, json.dumps(value))
        elif timeout:
            await self._pool.execute("setex", key, timeout, json.dumps(value))

    async def add(self, key: str, value: Serializable, *, timeout: Optional[int]):
        if timeout is None:
            await self._pool.execute("set", key, json.dumps(value), "nx")
        elif timeout:
            await self._pool.execute("set", key, json.dumps(value), "ex", timeout, "nx")

    async def get_or_set(
        self, key: str, default: Any, *, timeout: Optional[int]
    ) -> Any:
        value = await self.get(key, None)
        if value is None:
            await self.set(key, default, timeout=timeout)
            return default
        return value

    async def get_many(self, keys: Iterable[str]) -> Dict[str, Any]:
        values = await self._pool.execute("mget", *keys)
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
            await self._pool.execute("mset", *values)
        if timeout:
            expire = []
            for key in mapping:
                expire.append(self._pool.execute("expire", key, timeout))
            await asyncio.gather(*expire)

    async def delete(self, key: str):
        await self._pool.execute("unlink", key)

    async def delete_many(self, keys: Iterable[str]):
        await self._pool.execute("unlink", *keys)

    async def clear(self):
        await self._pool.execute("flushdb", "async")

    async def touch(self, key: str, timeout: Optional[int]) -> bool:
        if timeout is None:
            return bool(await self._pool.execute("persist", key))
        if timeout:
            return bool(await self._pool.execute("expire", key, timeout))
        return bool(await self._pool.execute("unlink", key))

    async def incr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        if not await self._pool.execute("exists", key):
            raise ValueError(f"'{key}' is not set in the cache")
        if isinstance(delta, int):
            return await self._pool.execute("incrby", key, delta)
        if isinstance(delta, float):
            return json.loads(await self._pool.execute("incrbyfloat", key, delta))
        raise ValueError(f"decr value must be int or float")

    async def decr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        if not await self._pool.execute("exists", key):
            raise ValueError(f"'{key}' is not set in the cache")
        if isinstance(delta, int):
            return await self._pool.execute("incrby", key, delta * -1)
        if isinstance(delta, float):
            return json.loads(
                await self._pool.execute("incrbyfloat", key, delta * -1.0)
            )
        raise ValueError(f"decr value must be int or float")
