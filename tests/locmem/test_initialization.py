import pytest

from caches import Cache


def test_locmem_cache_can_be_initialized_without_net_loc():
    cache = Cache("locmem://")


def test_locmem_cache_can_be_initialized_with_net_loc():
    cache = Cache("locmem://primary")


def test_locmem_cache_can_be_initialized_with_key_prefix():
    cache = Cache("locmem://", key_prefix="test")


def test_locmem_cache_can_be_initialized_with_timeout():
    cache = Cache("locmem://", timeout=600)


def test_locmem_cache_can_be_initialized_with_version():
    cache = Cache("locmem://", version=20)


@pytest.mark.asyncio
async def test_locmem_cache_uses_net_loc_for_separaing_namespaces():
    cache = Cache("locmem://")
    other_cache = Cache("locmem://other")

    await cache.connect()
    await other_cache.connect()

    await cache.set("test", "Ok!")
    assert await other_cache.get("test") is None
    assert await cache.get("test") == "Ok!"
