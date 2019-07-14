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


def test_cache_timeout_defaults_to_none(cache):
    assert cache.make_timeout() is None


def test_cache_timeout_can_be_set_per_key(cache):
    assert cache.make_timeout(100) == 100


def test_cache_can_be_set_default_timeout():
    cache = Cache("dummy://null", timeout=600)
    assert cache.make_timeout() == 600


def test_cache_can_be_set_default_timeout_in_url():
    cache = Cache("dummy://null?timeout=600")
    assert cache.make_timeout() == 600


def test_cache_default_timeout_can_be_overrided_per_key():
    cache = Cache("dummy://null", timeout=600)
    assert cache.make_timeout(120) == 120
