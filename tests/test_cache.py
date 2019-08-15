import pytest

from caches import Cache


@pytest.fixture
def cache():
    return Cache("dummy://null")


def test_cache_created_key_includes_app_key(cache):
    key = cache.make_key("test")
    assert "test" in key


def test_cache_created_key_includes_prefix():
    cache = Cache("dummy://null", key_prefix="prod")
    key = cache.make_key("test")
    assert key.startswith("prod")
    assert "test" in key


def test_cache_created_key_includes_default_version():
    cache = Cache("dummy://null", version="beta")
    key = cache.make_key("test")
    assert "beta" in key
    assert "test" in key


def test_cache_key_default_version_can_be_overridded():
    cache = Cache("dummy://null", version="beta")
    key = cache.make_key("test", "custom")
    assert "beta" not in key
    assert "custom" in key
    assert "test" in key


def test_cache_created_key_includes_prefix_and_version():
    cache = Cache("dummy://null", key_prefix="prod", version="2019")
    key = cache.make_key("test")
    assert key.startswith("prod")
    assert "2019" in key
    assert "test" in key


def test_cache_key_prefix_can_be_set_in_url():
    cache = Cache("dummy://null?key_prefix=prod")
    key = cache.make_key("test")
    assert key.startswith("prod")
    assert "test" in key


def test_cache_key_prefix_kwarg_overrides_key_prefix_be_set_in_url():
    cache = Cache("dummy://null?key_prefix=prod", key_prefix="beta")
    key = cache.make_key("test")
    assert key.startswith("beta")
    assert "prod" not in key
    assert "test" in key


def test_cache_version_can_be_set_in_url():
    cache = Cache("dummy://null?version=2019")
    key = cache.make_key("test")
    assert "2019" in key
    assert "test" in key


def test_cache_version_kwarg_overrides_version_set_in_url():
    cache = Cache("dummy://null?version=2019", version="2020")
    key = cache.make_key("test")
    assert "2019" not in key
    assert "2020" in key
    assert "test" in key


def test_cache_ttl_defaults_to_none(cache):
    assert cache.make_ttl() is None


def test_cache_ttl_can_be_set_per_key(cache):
    assert cache.make_ttl(100) == 100


def test_cache_can_be_set_default_ttl():
    cache = Cache("dummy://null", ttl=600)
    assert cache.make_ttl() == 600


def test_cache_can_be_set_default_ttl_in_url():
    cache = Cache("dummy://null?ttl=600")
    assert cache.make_ttl() == 600


def test_cache_default_ttl_can_be_overrided_per_key():
    cache = Cache("dummy://null", ttl=600)
    assert cache.make_ttl(120) == 120


def test_cache_errors_if_ttl_option_is_set_to_0():
    with pytest.raises(ValueError):
        Cache("dummy://null", ttl=0)


def test_cache_errors_if_ttl_option_in_url_is_set_to_0():
    with pytest.raises(ValueError):
        Cache("dummy://null?ttl=0")


def test_cache_errors_if_key_ttl_is_set_to_0():
    cache = Cache("dummy://null")
    with pytest.raises(ValueError):
        assert cache.make_ttl(0)


@pytest.mark.asyncio
async def test_cache_can_be_used_as_context_manager():
    async with Cache("locmem://") as cache:
        await cache.set("test", "Ok!")
        assert await cache.get("test") == "Ok!"
