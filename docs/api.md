# API reference

## `get`

```python
await cache.get(key: str, default: Any = None, *, version: Optional[Version] = None) -> Any
```

### Required arguments

#### `key`

String with cache key to read.


### Optional arguments

#### `default`

Default value that should be returned if key doesn't exist in the cache, or has expired.

Defaults to `None`.


#### `version`

Version of key that should be returned. String or integer.

Defaults to `None`, unless default version for set for the cache.


### Return value

Returns value that was set in cache or `default` if key wasn't found in cache, or has expired.