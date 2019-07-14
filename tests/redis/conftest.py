import pytest

from caches import Cache


@pytest.fixture
async def cache():
    obj = Cache("redis://localhost:6379/1")
    await obj.connect()
    await obj.clear()
    yield obj
    await obj.clear()
    await obj.disconnect()
