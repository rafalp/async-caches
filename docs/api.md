# API reference

## `Cache`

### `connect`

```python
await cache.connect()
```

Connects cache to server.


### `disconnect`

```python
await cache.disconnect()
```

Disconnects cache from server.


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

Defaults to `None`, unless default version for set for the cache.


### `set`

```python
await cache.set(key: str, value: Serializable, *, timeout: Optional[int] = None, version: Optional[Version] = None)
```

Sets new value for key in the cache. If key doesn't exist it will be created. 


#### Required arguments

##### `key`

String with cache key to set.


##### `value`

JSON-serializable value to store in the cache.


#### Optional arguments

##### `timeout`

Integer with number of seconds after which key will expire and will be removed by the cache. 

Defaults to `None` (cache forever), unless default timeout is set for cache.


##### `version`

Version of key that should be set. String or integer.

Defaults to `None`, unless default version for set for the cache.


### `add`

```python
await cache.add(key: str, value: Serializable, *, timeout: Optional[int] = None, version: Optional[Version] = None)
```

Sets new key in the cache. Does nothing if key already exists.


### `get_or_set`

```python
await cache.get_or_set(key: str, default: Serializable, *, timeout: Optional[int] = None, version: Optional[Version] = None) -> Any
```

Gets value for key from the cache. If key doesn't exist, it is set with `default` value.


### `get_many`

```python
await cache.get_many(keys: Iterable[str], version: Optional[Version] = None) -> Dict[str, Any]
```

Gets values for many keys from the cache in single read operation.


### `set_many`

```python
await cache.set_many(mapping: Mapping[str, Serializable], *, timeout: Optional[int] = None)
```

Sets values for many keys in the cache in single write operation.

> **Note:** if timeout argument is provided, second command will be ran to set keys expiration time on the cache server.


### `delete`

```python
await cache.delete(key: str, version: Optional[Version] = None)
```

Deletes key from the cache.


### `delete_many`

```python
await cache.delete_many(keys: Iterable[str], version: Optional[Version] = None)
```

Deletes many keys from the cache.


### `clear`

```python
await cache.clear()
```

Deletes all keys from the cache.

> **Note:** `cache.clear()` will remove all keys from cache, not just ones set by your application.
>
> Be careful when calling it, if your app shares Redis database with other clients.


### `touch`

```python
await cache.touch(key: str, timeout: Optional[int] = None, *, version: Optional[Version] = None) -> bool
```

Updates expiration time for the key.


### `incr`

```python
await cache.incr(key: str, delta: Union[float, int] = 1, *, version: Optional[Version] = None) -> Union[float, int]
```

Increases key in the cache by a value.


### `decr`

```python
await cache.decr(key: str, delta: Union[float, int] = 1, *, version: Optional[Version] = None) -> Union[float, int]
```

Increases key in the cache by a value.