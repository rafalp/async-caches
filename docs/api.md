# API reference

## `Cache`


### `connect`

```python
await cache.connect()
```

Connects cache to server.


- - -


### `disconnect`

```python
await cache.disconnect()
```

Disconnects cache from server.


- - -


### `get`

```python
await cache.get(key: str, default: Any = None, *, version: Optional[Version] = None) -> Any
```

Gets value for key from the cache.


#### Required arguments

##### `key`

String with cache key to read.


#### Optional arguments

##### `default`

Default value that should be returned if key doesn't exist in the cache, or has expired.

Defaults to `None`.


##### `version`

Version of key that should be returned. String or integer.

Defaults to `None`, unless default version is set for the cache.


- - -


### `set`

```python
await cache.set(key: str, value: Serializable, *, ttl: Optional[int] = None, version: Optional[Version] = None)
```

Sets new value for key in the cache. If key doesn't exist it will be created. 


#### Required arguments

##### `key`

String with cache key to set.


##### `value`

JSON-serializable value to store in the cache.


#### Optional arguments

##### `ttl`

Integer with number of seconds after which set key will expire and will be removed by the cache.

Defaults to `None` (cache forever), unless default `ttl` is set for cache.


##### `version`

Version of key that should be set. String or integer.

Defaults to `None`, unless default version is set for the cache.


- - -


### `add`

```python
await cache.add(key: str, value: Serializable, *, ttl: Optional[int] = None, version: Optional[Version] = None) -> bool
```

Sets key in the cache if it doesn't already exist, or has expired.


#### Required arguments

##### `key`

String with cache key to set.


##### `value`

JSON-serializable value to store in the cache.


#### Optional arguments

##### `ttl`

Integer with number of seconds after which set key will expire and will be removed by the cache. 

Defaults to `None` (cache forever), unless default ttl is set for cache.


##### `version`

Version of key that should be set. String or integer.

Defaults to `None`, unless default version is set for the cache.


#### Return value

Returns `True` if key was added to cache and `False` if it already exists.


- - -


### `get_or_set`

```python
await cache.get_or_set(key: str, default: Union[Awaitable, Serializable], *, ttl: Optional[int] = None, version: Optional[Version] = None) -> Any
```

Gets value for key from the cache. If key doesn't exist or has expired, new key is set with `default` value.


#### Required arguments

##### `key`

String with cache key to read or set.


##### `default`

Default value that should be returned if key doesn't exist in the cache, or has expired. It has to be JSON-serializable and will be set in cache if read didn't return the value.

If `default` is callable, it will be called and it's return value will be set in cache.


#### Optional arguments

##### `ttl`

Integer with number of seconds after which set key will expire and will be removed by the cache. 

Defaults to `None` (cache forever), unless default ttl is set for cache.


##### `version`

Version of key that should be get (or set). String or integer.

Defaults to `None`, unless default version is set for the cache.


#### Return value

Returns key value from cache if it exists, or `default` otherwise.


- - -


### `get_many`

```python
await cache.get_many(keys: Iterable[str], version: Optional[Version] = None) -> Dict[str, Any]
```

Gets values for many keys from the cache in single read operation.


#### Required arguments

##### `keys`

List or tuple of string with cache keys to read.


#### Optional arguments

##### `version`

Version of keys that should be get from the cache. String or integer.

Defaults to `None`, unless default version is set for the cache.


#### Return value

Returns dict of cache-returned values. If any of keys didn't exist in the cache or was expired, it's value will be as `None`.


- - -


### `set_many`

```python
await cache.set_many(mapping: Mapping[str, Serializable], *, ttl: Optional[int] = None)
```

Sets values for many keys in the cache in single write operation.

> **Note:** if ttl argument is provided, second command will be ran to set keys expiration time on the cache server.


- - -


### `delete`

```python
await cache.delete(key: str, version: Optional[Version] = None)
```

Deletes the key from the cache. Does nothing if the key doesn't exist.


#### Required arguments

##### `key`

Key to delete from cache.


#### Optional arguments

##### `version`

Version of key that should be deleted from the cache. String or integer.

Defaults to `None`, unless default version is set for the cache.


- - -


### `delete_many`

```python
await cache.delete_many(keys: Iterable[str], version: Optional[Version] = None)
```

Deletes many keys from the cache. Skips keys that don't exist.


#### Required arguments

##### `keys`

Keys to delete from cache.


#### Optional arguments

##### `version`

Version of keys that should be deleted from the cache. String or integer.

Defaults to `None`, unless default version is set for the cache.


- - -


### `clear`

```python
await cache.clear()
```

Deletes all keys from the cache.

> **Note:** `cache.clear()` will remove all keys from cache, not just ones set by your application.
>
> Be careful when calling it, if your app shares Redis database with other clients.


- - -


### `touch`

```python
await cache.touch(key: str, ttl: Optional[int] = None, *, version: Optional[Version] = None) -> bool
```

Updates expiration time for the key.


#### Required arguments

##### `key`

String with cache key which ttl value should be updated.


#### Optional arguments

##### `ttl`

Integer with number of seconds after which updated key will expire and will be removed by the cache, or `None` if key should never expire.

Defaults to `None` (cache forever), unless default ttl is set for cache.


##### `version`

Version of key that should be updated. String or integer.

Defaults to `None`, unless default version is set for the cache.


#### Return value

Returns `True` if key's expirat was updated, and `False` if key didn't exist in the cache.


- - -


### `incr`

```python
await cache.incr(key: str, delta: Union[float, int] = 1, *, version: Optional[Version] = None) -> Union[float, int]
```

Increases the value stored for specified key by specified amount.


#### Required arguments

##### `key`

String with cache key which should be updated.


#### Optional arguments

##### `delta`

Amount by which key value should be increased. Can be `float` or `int`.

Defaults to `1`.


##### `version`

Version of key that should be updated. String or integer.

Defaults to `None`, unless default version is set for the cache.


#### Return value

Returns `float` or `int` with updated value. If key didn't exist, this value will equal to value passed in delta argument.


- - -


### `decr`

```python
await cache.decr(key: str, delta: Union[float, int] = 1, *, version: Optional[Version] = None) -> Union[float, int]
```

Decreases the value stored for specified key by specified amount.


#### Required arguments

##### `key`

String with cache key which should be updated.


#### Optional arguments

##### `delta`

Amount by which key value should be decreased. Can be `float` or `int`.

Defaults to `1`.


##### `version`

Version of key that should be updated. String or integer.

Defaults to `None`, unless default version is set for the cache.


#### Return value

Returns `float` or `int` with updated value. If key didn't exist, this value will equal to value passed in delta argument.