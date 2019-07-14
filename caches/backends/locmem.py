import json
from inspect import isawaitable
from time import time
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, Union

from ..types import Serializable
from .base import BaseBackend


class LocMemBackend(BaseBackend):
    _caches: Dict[str, Dict[str, Tuple[Any, Optional[int]]]] = {}

    async def connect(self):
        # pylint: disable=attribute-defined-outside-init
        self._id = self._cache_url.netloc or "_"
        self._caches[self._id] = {}
        return True

    async def disconnect(self):
        self._caches.pop(self._id)
        return True

    async def get(self, key: str, default: Any) -> Any:
        if key not in self._caches[self._id]:
            return default

        value, timeout = self._caches[self._id][key]
        if timeout and timeout < time():
            return default

        return json.loads(value)

    async def set(
        self, key: str, value: Serializable, *, timeout: Optional[int]
    ) -> Any:
        if timeout is not None:
            timeout += int(time())
        self._caches[self._id][key] = json.dumps(value), timeout

    async def add(self, key: str, value: Serializable, *, timeout: Optional[int]):
        if key not in self._caches[self._id]:
            await self.set(key, value, timeout=timeout)

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
        return {key: await self.get(key, None) for key in keys}

    async def set_many(
        self, mapping: Mapping[str, Serializable], *, timeout: Optional[int]
    ):
        for k, v in mapping.items():
            await self.set(k, v, timeout=timeout)

    async def delete(self, key: str):
        self._caches[self._id].pop(key, None)

    async def delete_many(self, keys: Iterable[str]):
        for key in keys:
            self._caches[self._id].pop(key, None)

    async def clear(self):
        self._caches[self._id] = {}

    async def touch(self, key: str, timeout: Optional[int]) -> bool:
        if key not in self._caches[self._id]:
            return False
        if timeout is not None:
            timeout += int(time())

        value, _ = self._caches[self._id][key]
        self._caches[self._id][key] = value, timeout
        return True

    async def incr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        if key not in self._caches[self._id]:
            raise ValueError(f"'{key}' is not set in the cache")
        if not isinstance(delta, (float, int)):
            raise ValueError(f"incr value must be int or float")

        value, timeout = self._caches[self._id][key]
        value = json.loads(value) + delta
        self._caches[self._id][key] = json.dumps(value), timeout
        return value

    async def decr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        if key not in self._caches[self._id]:
            raise ValueError(f"'{key}' is not set in the cache")
        if not isinstance(delta, (float, int)):
            raise ValueError(f"decr value must be int or float")

        value, timeout = self._caches[self._id][key]
        value = json.loads(value) - delta
        self._caches[self._id][key] = json.dumps(value), timeout
        return value
