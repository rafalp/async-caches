import asyncio
import json
from typing import Any, Dict, Iterable, Mapping, Optional, Union

import aioredis

from ..types import Serializable
from .base import BaseBackend


class RedisBackend(BaseBackend):
    async def connect(self):
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
        raise NotImplementedError()

    async def get_many(self, keys: Iterable[str]) -> Dict[str, Any]:
        raise NotImplementedError()

    async def set_many(
        self, mapping: Mapping[str, Serializable], *, timeout: Optional[int]
    ):
        raise NotImplementedError()

    async def delete(self, key: str):
        raise NotImplementedError()

    async def delete_many(self, keys: Iterable[str]):
        raise NotImplementedError()

    async def clear(self):
        await self._pool.execute("flushdb", "async")

    async def touch(self, key: str, timeout: Optional[int]) -> bool:
        raise NotImplementedError()

    async def incr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        raise NotImplementedError()

    async def decr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        raise NotImplementedError()
