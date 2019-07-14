# Backends

Async Caches ships with three caching backends, each intended for different usage:


## Dummy cache

Dummy cache backend that doesn't cache anything. Enables you to easily disable caching without having to litter your code with conditions and checks. It also checks if values passed to cache are JSON-serializable.

```python
from caches import Cache


cache = Cache("dummy://null")
```

> **Note:** Because dummy backend has no configuration options, it doesn't matter what you'll write after the `dummy://` part.


## Local memory cache

Cache backend that stores data in local memory. Lets you develop and test caching without need for actual cache server. Its purged when application restarts, so you don't have to spend time invalidating caches when changing your app.

This backend supports cache versions and timeouts.

```python
from caches import Cache


cache = Cache("locmem://null")
```


## Redis

This backend stores data on Redis server. This is only backend intended for *actual* use on production. It supports key prefixes, versions and timeouts.


```python
from caches import Cache


# Connection to locally running Redis instance
cache = Cache("redis://localhost")
```


## Connection

To use cache, it has to be *connected*. After cache is no longer needed, it should be *disconnected*.

> **Note:** running event loop is required for cache to work. 

```python
async def myapp():
    cache = Cache("redis://localhost")
    await cache.connect()
    await cache.set("test", "Ok!")
    await cache.disconnect()
```

Alternatively, cache may be used as context manager:

```python
async def myapp():
    async with Cache("redis://localhost") as cache:
        await cache.set("test", "Ok!")
```


## Configuration


### Multiple instances

All cache backends support running multiple cache instances:

```python
from caches import Cache


# Multiple Redis instances
default = Cache("redis://localhost")
user_tracker = Cache("redis://localhost/1")


# Multiple locmemory instances
default = Cache("locmem://default")
user_tracker = Cache("locmem://users")


# Multiple dummy instances
default = Cache("dummy://default")
user_tracker = Cache("dummy://users")
```


### Setting options

Options can be set either as elements of querystring in cache URL, or as extra kwargs passed to `Cache`:

```python
from caches import Cache


# Option included in cache link...
cache = Cache("redis://localhost?timeout=600")


# ...and set as kwarg
cache = Cache("locmem://default", timeout=600)
```

> **Note:** when option is set in both URL and kwarg, the URL value is discarded. 


### Default timeout

By default cache keys never expire, unless expiration time was explicitly set for a specific key.

You can override this behaviour by setting default timeout (in seconds) for all keys on cache:

```python
from caches import Cache


# Expire keys after 5 minutes.
cache = Cache("redis://localhost", timeout=600)
```


### Default version

By default cache keys are not versioned, unless version was specified during key set.

You can default keys to specific version using `version` option:

```python
from caches import Cache


# Version can be an integer...
cache = Cache("redis://localhost", version=2019)


# ...or a string
cache = Cache("redis://localhost", version="f6s8a68687as")
```


### Default key prefix

If your cache shares Redis database with other clients, you can prefix your cache keys with string specific to your client to reduce chance of key collision:

```python
from caches import Cache


cache = Cache("redis://localhost/0", key_prefix="forum")
```

> **Note:** Clearing your cache by calling `cache.clear()` will remove all keys from cache, regardless of their prefix.


### Connections pool size

Redis backend supports `maxsize` and `minsize` options that can be used to configure size of available connections pool used by the cache to communicate with the Redis server:

```python
from caches import Cache


cache = Cache("redis://localhost", minsize=2, maxsize=5)
```

> **Note:** Redis backend defaults to 1 min. and 10 max. connections.