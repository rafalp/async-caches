from typing import Any, Dict, Iterable, Mapping, Optional, Union

from ..core import CacheURL
from ..types import Serializable


class BaseBackend:
    def __init__(self, cache_url: Union[CacheURL, str], **options: Any):
        self._cache_url = CacheURL(cache_url)
        self._options = options

    async def connect(self):
        raise NotImplementedError()

    async def disconnect(self):
        raise NotImplementedError()

    async def get(self, key: str, default: Any) -> Any:
        raise NotImplementedError()

    async def set(
        self, key: str, value: Serializable, *, timeout: Optional[int]
    ) -> Any:
        raise NotImplementedError()

    async def add(self, key: str, value: Serializable, *, timeout: Optional[int]):
        raise NotImplementedError()

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
        raise NotImplementedError()

    async def touch(self, key: str, timeout: Optional[int]) -> bool:
        raise NotImplementedError()

    async def incr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        raise NotImplementedError()

    async def decr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        raise NotImplementedError()
