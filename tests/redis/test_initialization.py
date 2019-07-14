from unittest.mock import Mock

import pytest

from caches import Cache
from caches.backends.redis import RedisBackend


@pytest.mark.asyncio
async def test_backend_errors_if_more_than_one_connection_is_opened():
    cache = Cache("redis://localhost/1")
    await cache.connect()
    with pytest.raises(AssertionError):
        await cache.connect()
    await cache.disconnect()


@pytest.mark.asyncio
async def test_backend_errors_if_nonexistant_connection_is_closed():
    cache = Cache("redis://localhost/1")
    with pytest.raises(AssertionError):
        await cache.disconnect()


@pytest.mark.asyncio
async def test_connections_pool_minsize_can_be_set_in_url():
    cache = RedisBackend("redis://localhost/1?minsize=2")
    kwargs = cache._get_connection_kwargs()
    assert kwargs["minsize"] == 2


@pytest.mark.asyncio
async def test_connections_pool_minsize_can_be_set_in_kwarg():
    cache = RedisBackend("redis://localhost/1", minsize=2)
    kwargs = cache._get_connection_kwargs()
    assert kwargs["minsize"] == 2


@pytest.mark.asyncio
async def test_connections_pool_minsize_kwarg_overrides_value_from_url():
    cache = RedisBackend("redis://localhost/1?minsize=2", minsize=3)
    kwargs = cache._get_connection_kwargs()
    assert kwargs["minsize"] == 3


@pytest.mark.asyncio
async def test_connections_pool_maxsize_can_be_set_in_url():
    cache = RedisBackend("redis://localhost/1?maxsize=2")
    kwargs = cache._get_connection_kwargs()
    assert kwargs["maxsize"] == 2


@pytest.mark.asyncio
async def test_connections_pool_maxsize_can_be_set_in_kwarg():
    cache = RedisBackend("redis://localhost/1", maxsize=2)
    kwargs = cache._get_connection_kwargs()
    assert kwargs["maxsize"] == 2


@pytest.mark.asyncio
async def test_connections_pool_maxsize_kwarg_overrides_value_from_url():
    cache = RedisBackend("redis://localhost/1?maxsize=2", maxsize=3)
    kwargs = cache._get_connection_kwargs()
    assert kwargs["maxsize"] == 3
