import pytest

from caches import Cache
from caches.backends.base import BaseBackend


@pytest.fixture
def cache():
    return BaseBackend("base://null")


def test_cache_cant_be_initialized_with_base_backend():
    with pytest.raises(AssertionError):
        Cache("base://null")


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_connecting(cache):
    with pytest.raises(NotImplementedError):
        await cache.connect()


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_disconnecting(cache):
    with pytest.raises(NotImplementedError):
        await cache.disconnect()


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_getting_keys(cache):
    with pytest.raises(NotImplementedError):
        await cache.get("test", None)


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_setting_keys(cache):
    with pytest.raises(NotImplementedError):
        await cache.set("test", "Ok!", ttl=0)


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_adding_keys(cache):
    with pytest.raises(NotImplementedError):
        await cache.add("test", "Ok!", ttl=0)


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_get_or_set_keys(cache):
    with pytest.raises(NotImplementedError):
        await cache.get_or_set("test", "Ok!", ttl=0)


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_getting_many_keys(cache):
    with pytest.raises(NotImplementedError):
        await cache.get_many(["test", "other"])


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_setting_many_keys(cache):
    with pytest.raises(NotImplementedError):
        await cache.set_many({"test": "Ok!", "hello": "World!"}, ttl=0)


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_deleting_keys(cache):
    with pytest.raises(NotImplementedError):
        await cache.delete("test")


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_deleting_many_keys(cache):
    with pytest.raises(NotImplementedError):
        await cache.delete_many(["test", "hello"])


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_clearing(cache):
    with pytest.raises(NotImplementedError):
        await cache.clear()


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_touch(cache):
    with pytest.raises(NotImplementedError):
        await cache.touch("test", 0)


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_incrementing(cache):
    with pytest.raises(NotImplementedError):
        await cache.incr("test", 1)


@pytest.mark.asyncio
async def test_base_backend_doesnt_implement_decrementing(cache):
    with pytest.raises(NotImplementedError):
        await cache.decr("test", 1)
