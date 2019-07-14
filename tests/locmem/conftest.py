import pytest

from caches import Cache


@pytest.fixture
async def cache():
    obj = Cache("locmem://0")
    await obj.connect()
    return obj
