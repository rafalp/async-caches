from caches.core import CacheURL


def test_backend_is_taken_from_url_protocol():
    url = CacheURL("dummy://")
    assert url.backend == "dummy"


def test_hostname_is_taken_from_url():
    url = CacheURL("dummy://localhost")
    assert url.hostname == "localhost"


def test_none_is_returned_for_hostname_if_its_not_set():
    url = CacheURL("dummy://")
    assert url.hostname is None


def test_port_is_taken_from_url():
    url = CacheURL("redis://localhost:6379")
    assert url.port == 6379


def test_none_is_returned_for_port_if_its_not_set():
    url = CacheURL("redis://localhost")
    assert url.port is None


def test_netloc_is_taken_from_url():
    url = CacheURL("redis://localhost:6379")
    assert url.netloc == "localhost:6379"


def test_none_is_returned_for_netloc_if_its_not_set():
    url = CacheURL("redis://")
    assert url.netloc is None


def test_database_is_taken_from_url():
    url = CacheURL("redis://localhost/0")
    assert url.database == "0"


def test_none_is_returned_for_database_if_its_not_set():
    url = CacheURL("redis://localhost/")
    assert url.database is None


def test_url_obj_can_be_converted_back_to_str():
    url_str = "redis://localhost:6379"
    url = CacheURL(url_str)
    assert str(url) == url_str


def test_url_obj_has_repr():
    url = CacheURL("dummy://")
    assert repr(url)


def test_url_obj_can_be_compared_to_str():
    url_str = "redis://localhost:6379"
    url = CacheURL(url_str)
    assert url == url_str
    assert url != "dummy://"


def test_url_obj_can_be_compared_to_other_url_obj():
    url_str = "redis://localhost:6379"
    assert CacheURL(url_str) == CacheURL(url_str)
    assert CacheURL(url_str) != CacheURL("dummy://")
