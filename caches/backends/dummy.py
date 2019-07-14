from inspect import isawaitable
from typing import Any, Dict, Iterable, Mapping, Optional, Union

from ..types import Serializable
from .base import BaseBackend


class DummyBackend(BaseBackend):
    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def get(self, key: str, default: Any) -> Any:
        return default

    async def set(
        self, key: str, value: Serializable, *, timeout: Optional[int]
    ) -> Any:
        pass

    async def add(self, key: str, value: Serializable, *, timeout: Optional[int]):
        pass

    async def get_or_set(
        self,
        key: str,
        default: Any,
        *,
        timeout: Optional[int],  # pylint: disable=unused-argument
    ) -> Any:
        if callable(default):
            default = default()
            if isawaitable(default):
                default = await default
        return default

    async def get_many(self, keys: Iterable[str]) -> Dict[str, Any]:
        return {key: None for key in keys}

    async def set_many(
        self, mapping: Mapping[str, Serializable], *, timeout: Optional[int]
    ):
        pass

    async def delete(self, key: str):
        pass

    async def delete_many(self, keys: Iterable[str]):
        pass

    async def clear(self):
        pass

    async def touch(self, key: str, timeout: Optional[int]) -> bool:
        return False

    async def incr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        raise ValueError(f"'{key}' is not set in the cache")

    async def decr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        raise ValueError(f"'{key}' is not set in the cache")
