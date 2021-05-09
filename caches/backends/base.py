import json
from abc import ABCMeta, abstractmethod
from typing import Any, Awaitable, Dict, Iterable, Mapping, Optional, Union

from ..core import CacheURL
from ..types import Serializable


class BaseBackend(metaclass=ABCMeta):
    def __init__(self, cache_url: Union[CacheURL, str], **options: Any):
        self._cache_url = CacheURL(cache_url)
        self._options = options

    @abstractmethod
    async def connect(self):
        raise NotImplementedError()

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError()

    @abstractmethod
    async def get(self, key: str, default: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def set(self, key: str, value: Serializable, *, ttl: Optional[int]) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def add(self, key: str, value: Serializable, *, ttl: Optional[int]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def get_or_set(
        self, key: str, default: Union[Awaitable[Serializable], Serializable], *, ttl: Optional[int]
    ) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def get_many(self, keys: Iterable[str]) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    async def set_many(
        self, mapping: Mapping[str, Serializable], *, ttl: Optional[int]
    ):
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    async def delete_many(self, keys: Iterable[str]):
        raise NotImplementedError()

    @abstractmethod
    async def clear(self):
        raise NotImplementedError()

    @abstractmethod
    async def touch(self, key: str, ttl: Optional[int]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def incr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        raise NotImplementedError()

    @abstractmethod
    async def decr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        raise NotImplementedError()

    @staticmethod
    def _serialize(value: Any) -> str:
        """Serializes value to string.

        Args:
            value (Any): Whatever to serialize.

        Returns:
            str: Serialized value to string.
        """
        return json.dumps(value)

    @staticmethod
    def _deserialize(value: str) -> Any:
        """Deserializes value to original data structure.

        Args:
            value (str): Serialized value

        Returns:
            Any: Original data
        """
        return json.loads(value)
