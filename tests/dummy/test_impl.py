import pytest


@pytest.mark.asyncio
async def test_setting_key_is_noop(cache):
    await cache.set("test", "Ok!")
    assert await cache.get("test") is None


@pytest.mark.asyncio
async def test_versioning_key_is_noop(cache):
    await cache.set("test", "Ok!", version=1)
    await cache.set("test", "Nope!", version=2)
    assert await cache.get("test", version=1) is None
    assert await cache.get("test", version=2) is None


@pytest.mark.asyncio
async def test_default_is_returned_when_set(cache):
    assert await cache.get("text", "default") == "default"


@pytest.mark.asyncio
async def test_adding_key_is_noop(cache):
    await cache.add("test", "Ok!")
    assert await cache.get("test") is None


@pytest.mark.asyncio
async def test_adding_key_always_returns_false(cache):
    assert await cache.add("test", "Ok!") is False


@pytest.mark.asyncio
async def test_key_get_or_set_is_noop(cache):
    assert await cache.get_or_set("test", "Ok!") == "Ok!"


@pytest.mark.asyncio
async def test_key_get_or_set_callable_default_is_called(cache):
    def default():
        return "Ok!"

    assert await cache.get_or_set("test", default) == "Ok!"


@pytest.mark.asyncio
async def test_key_get_or_set_async_callable_default_is_called_and_awaited(cache):
    async def default():
        return "Ok!"

    assert await cache.get_or_set("test", default) == "Ok!"


@pytest.mark.asyncio
async def test_getting_many_keys_always_returns_nothing(cache):
    await cache.set("test", "Ok!")
    values = await cache.get_many(["test", "undefined"])
    assert len(values) == 2
    assert values["test"] is None
    assert values["undefined"] is None


@pytest.mark.asyncio
async def test_setting_many_keys_is_noop(cache):
    await cache.set_many({"test": "Ok!", "hello": "world"})
    assert await cache.get("test") is None
    assert await cache.get("hello") is None


@pytest.mark.asyncio
async def test_deleting_key_is_noop(cache):
    await cache.set("test", "Ok!")
    await cache.delete("test")
    assert await cache.get("test") is None


@pytest.mark.asyncio
async def test_deleting_many_keys_is_noop(cache):
    await cache.set("test", "Ok!")
    await cache.delete_many(["test", "undefined"])
    assert await cache.get("test") is None
    assert await cache.get("undefined") is None


@pytest.mark.asyncio
async def test_clearing_is_noop(cache):
    await cache.clear()


@pytest.mark.asyncio
async def test_touch_is_noop_for_set_key(cache):
    await cache.set("test", "Ok!", timeout=0)
    assert await cache.touch("test") is False


@pytest.mark.asyncio
async def test_touch_is_noop_for_undefined_key(cache):
    assert await cache.touch("undefined", 10) is False


@pytest.mark.asyncio
async def test_increasing_set_key_raises_value_error(cache):
    await cache.set("test", 10)
    with pytest.raises(ValueError):
        await cache.incr("test")


@pytest.mark.asyncio
async def test_increasing_key_raises_value_error(cache):
    with pytest.raises(ValueError):
        await cache.incr("test")


@pytest.mark.asyncio
async def test_decreasing_set_key_raises_value_error(cache):
    await cache.set("test", 10)
    with pytest.raises(ValueError):
        await cache.decr("test")


@pytest.mark.asyncio
async def test_decreasing_key_raises_value_error(cache):
    with pytest.raises(ValueError):
        await cache.decr("test")
