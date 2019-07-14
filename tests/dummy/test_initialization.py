import pytest

from caches import Cache


def test_dummy_cache_can_be_initialized_without_net_loc():
    Cache("dummy://")


def test_dummy_cache_can_be_initialized_with_net_loc():
    Cache("dummy://primary")


def test_dummy_cache_can_be_initialized_with_key_prefix():
    Cache("dummy://", key_prefix="test")


def test_dummy_cache_can_be_initialized_with_timeout():
    Cache("dummy://", timeout=600)


def test_dummy_cache_can_be_initialized_with_version():
    Cache("dummy://", version=20)


@pytest.mark.asyncio
async def test_dummy_cache_can_be_connected_and_disconnected():
    cache = Cache("dummy://", version=20)
    await cache.connect()
    await cache.disconnect()
