# API reference

## `Cache`

### `connect`


### `disconnect`


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


### `get_or_set`

```python
await cache.get_or_set(key: str, default: Any, *, timeout: Optional[int] = None, version: Optional[Version] = None) -> Any
```


### `get_many`

```python
await cache.get_many(keys: Iterable[str], version: Optional[Version] = None) -> Dict[str, Any]
```


### `set_many`

```python
await cache.set_many(mapping: Mapping[str, Serializable], *, timeout: Optional[int] = None)
```


### `delete`

```python
await cache.delete(key: str, version: Optional[Version] = None)
```


### `delete_many`

```python
await cache.delete_many(keys: Iterable[str], version: Optional[Version] = None)
```


### `clear`

```python
await cache.clear(self)
```


### `touch`

```python
await cache.touch(key: str, timeout: Optional[int] = None, *, version: Optional[Version] = None) -> bool
```


### `incr`

```python
await cache.incr(key: str, delta: Union[float, int] = 1, *, version: Optional[Version] = None) -> Union[float, int]
```


### `decr`

```python
await cache.decr(key: str, delta: Union[float, int] = 1, *, version: Optional[Version] = None) -> Union[float, int]
```