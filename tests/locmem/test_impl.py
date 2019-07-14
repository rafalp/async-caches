import pytest


@pytest.mark.asyncio
async def test_set_key_can_be_get(cache):
    await cache.set("test", "Ok!")
    assert await cache.get("test") == "Ok!"


@pytest.mark.asyncio
async def test_set_key_can_be_dict(cache):
    await cache.set("test", {"hello": "world"})
    assert await cache.get("test") == {"hello": "world"}


@pytest.mark.asyncio
async def test_set_key_can_be_list(cache):
    await cache.set("test", ["hello", "world"])
    assert await cache.get("test") == ["hello", "world"]


@pytest.mark.asyncio
async def test_key_can_be_versioned(cache):
    await cache.set("test", "Ok!", version=1)
    await cache.set("test", "Nope!", version=2)
    assert await cache.get("test", version=1) == "Ok!"
    assert await cache.get("test", version=2) == "Nope!"


@pytest.mark.asyncio
async def test_none_is_returned_for_expired_key(cache):
    await cache.set("test", "Ok!", timeout=0)
    assert await cache.get("test") is None


@pytest.mark.asyncio
async def test_none_is_returned_for_nonexistant_key(cache):
    assert await cache.get("nonexistant") is None


@pytest.mark.asyncio
async def test_none_is_returned_for_nonexistant_version(cache):
    await cache.set("test", "Ok!")
    assert await cache.get("test", version=2) is None


@pytest.mark.asyncio
async def test_default_is_returned_for_expired_key(cache):
    await cache.set("test", "Ok!", timeout=0)
    assert await cache.get("text", "default") == "default"


@pytest.mark.asyncio
async def test_default_is_returned_for_nonexistant_key(cache):
    assert await cache.get("nonexistant", "default") == "default"


@pytest.mark.asyncio
async def test_default_is_returned_for_nonexistant_version(cache):
    await cache.set("test", "Ok!")
    assert await cache.get("text", "default", version=2) == "default"


@pytest.mark.asyncio
async def test_key_can_be_added(cache):
    await cache.add("test", "Ok!")
    assert await cache.get("test") == "Ok!"


@pytest.mark.asyncio
async def test_key_can_be_added_with_timeout(cache):
    await cache.add("test", "Ok!", timeout=0)
    assert await cache.get("test") is None


@pytest.mark.asyncio
async def test_key_is_not_added_if_its_already_set(cache):
    await cache.set("test", "Initial")
    await cache.add("test", "Ok!")
    assert await cache.get("test") == "Initial"


@pytest.mark.asyncio
async def test_key_get_or_set_sets_given_value_if_key_is_undefined(cache):
    assert await cache.get_or_set("test", "Ok!") == "Ok!"
    assert await cache.get("test") == "Ok!"


@pytest.mark.asyncio
async def test_key_get_or_set_returns_previously_set_value(cache):
    await cache.set("test", "Ok!")
    assert await cache.get_or_set("test", "New") == "Ok!"


@pytest.mark.asyncio
async def test_key_get_or_set_is_not_overwriting_previously_set_value(cache):
    await cache.set("test", "Ok!")
    assert await cache.get_or_set("test", "New") == "Ok!"
    assert await cache.get("test") == "Ok!"


@pytest.mark.asyncio
async def test_key_get_or_set_overwrites_expired_key(cache):
    await cache.set("test", "Ok!", timeout=0)
    assert await cache.get_or_set("test", "New") == "New"
    assert await cache.get("test") == "New"


@pytest.mark.asyncio
async def test_many_keys_can_be_get(cache):
    await cache.set("test", "Ok!")
    await cache.set("hello", "world")
    values = await cache.get_many(["test", "hello"])
    assert len(values) == 2
    assert values["test"] == "Ok!"
    assert values["hello"] == "world"


@pytest.mark.asyncio
async def test_many_undefined_keys_are_returned_as_none(cache):
    await cache.set("test", "Ok!")
    values = await cache.get_many(["test", "undefined"])
    assert len(values) == 2
    assert values["test"] == "Ok!"
    assert values["undefined"] is None


@pytest.mark.asyncio
async def test_many_expired_keys_are_returned_as_none(cache):
    await cache.set("test", "Ok!")
    await cache.set("expired", "Ok!", timeout=0)
    values = await cache.get_many(["test", "expired"])
    assert len(values) == 2
    assert values["test"] == "Ok!"
    assert values["expired"] is None


@pytest.mark.asyncio
async def test_many_keys_can_be_set(cache):
    await cache.set_many({"test": "Ok!", "hello": "world"})
    assert await cache.get("test") == "Ok!"
    assert await cache.get("hello") == "world"


@pytest.mark.asyncio
async def test_many_keys_can_be_set_with_timeout(cache):
    await cache.set_many({"test": "Ok!", "hello": "world"}, timeout=0)
    assert await cache.get("test") is None
    assert await cache.get("hello") is None


@pytest.mark.asyncio
async def test_set_key_can_be_deleted(cache):
    await cache.set("test", "Ok!")
    await cache.delete("test")
    assert await cache.get("test") is None


@pytest.mark.asyncio
async def test_deleting_undefined_key_has_no_errors(cache):
    await cache.delete("undefined")


@pytest.mark.asyncio
async def test_many_set_keys_can_be_deleted(cache):
    await cache.set("test", "Ok!")
    await cache.set("hello", "world")
    await cache.delete_many(["test", "hello"])
    assert await cache.get("test") is None
    assert await cache.get("hello") is None


@pytest.mark.asyncio
async def test_deleting_many_undefined_keys_has_no_errors(cache):
    await cache.set("test", "Ok!")
    await cache.delete_many(["test", "undefined"])
    assert await cache.get("test") is None
    assert await cache.get("undefined") is None


@pytest.mark.asyncio
async def test_set_keys_are_cleared(cache):
    await cache.set("test", "Ok!")
    await cache.set("hello", "world")
    await cache.clear()
    assert await cache.get("test") is None
    assert await cache.get("hello") is None


@pytest.mark.asyncio
async def test_touch_removes_expired_key_timeout(cache):
    await cache.set("test", "Ok!", timeout=0)
    assert await cache.touch("test") is True
    assert await cache.get("test") == "Ok!"


@pytest.mark.asyncio
async def test_touch_updates_expired_key_timeout(cache):
    await cache.set("test", "Ok!", timeout=0)
    assert await cache.touch("test", 10) is True
    assert await cache.get("test") == "Ok!"


@pytest.mark.asyncio
async def test_touch_does_nothing_for_nonexistant_key(cache):
    assert await cache.touch("undefined", 10) is False
    assert await cache.get("undefined") is None


@pytest.mark.asyncio
async def test_set_key_can_be_increased(cache):
    await cache.set("test", 10)
    assert await cache.incr("test") == 11


@pytest.mark.asyncio
async def test_set_key_can_be_increased_by_int_value(cache):
    await cache.set("test", 10)
    assert await cache.incr("test", 2) == 12


@pytest.mark.asyncio
async def test_set_key_can_be_increased_by_float_value(cache):
    await cache.set("test", 10.0)
    assert await cache.incr("test", 2.5) == 12.5


@pytest.mark.asyncio
async def test_increasing_undefined_key_raises_value_error(cache):
    with pytest.raises(ValueError):
        await cache.incr("test")


@pytest.mark.asyncio
async def test_set_key_can_be_decreased(cache):
    await cache.set("test", 10)
    assert await cache.decr("test") == 9


@pytest.mark.asyncio
async def test_set_key_can_be_decreased_by_int_value(cache):
    await cache.set("test", 10)
    assert await cache.decr("test", 2) == 8


@pytest.mark.asyncio
async def test_set_key_can_be_decreased_by_float_value(cache):
    await cache.set("test", 10.0)
    assert await cache.decr("test", 2.5) == 7.5


@pytest.mark.asyncio
async def test_decreasing_undefined_key_raises_value_error(cache):
    with pytest.raises(ValueError):
        await cache.decr("test")
