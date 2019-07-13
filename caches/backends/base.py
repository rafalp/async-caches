from typing import Any, Optional, Union

from ..core import CacheURL
from ..types import Serializable, Version


class BaseBackend:
    def __init__(self, cache_url: Union[CacheURL, str], **options: typing.Any):
        self._cache_url = CacheURL(cache_url)
        self._options = options

    async def connect(self):
        raise NotImplementedError()

    async def disconnect(self):
        raise NotImplementedError()

    def make_key(self, key: str, version: Optional[Version] = None) -> str:
        pass

    async def get(
        self, key: str, default: Any, *, version: Optional[Version] = None
    ) -> Any:
        raise NotImplementedError()

    async def set(
        self, key: str, value: Serializable, *, version: Optional[Version] = None
    ) -> Any:
        raise NotImplementedError()
