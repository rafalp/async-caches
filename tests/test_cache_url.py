from caches.core import CacheURL


def test_protocol_is_available_as_backend():
    cache = CacheURL("dummy://null")
    assert cache.dialect == "dummy"
