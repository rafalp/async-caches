# API reference

## `Cache`

### `get`

```python
await cache.get(key: str, default: Any = None, *, version: Optional[Version] = None) -> Any
```

Gets value for key from cache.


#### Required arguments

##### `key`

String with cache key to read.


#### Optional arguments

##### `default`

Default value that should be returned if key doesn't exist in the cache, or has expired.

Defaults to `None`.


##### `version`

Version of key that should be returned. String or integer.

Defaults to `None`, unless default version for set for the cache.


### `set`

```python
await cache.set(self, key: str, value: Serializable, *, timeout: Optional[int] = None, version: Optional[Version] = None)
```

Sets new value for key in cache. If key doesn't exist it will be created. 


#### Required arguments

##### `key`

String with cache key to set.


##### `value`

JSON-serializable value to store in cache.


#### Optional arguments

##### `timeout`

Integer with number of seconds after which key will expire and will be removed by the cache. 

Defaults to `None` (cache forever), unless default timeout is set for cache.


##### `version`

Version of key that should be set. String or integer.

Defaults to `None`, unless default version for set for the cache.
