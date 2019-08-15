# Changelog

## 0.3 (15.08.2019)

- Renamed `timeout` to `ttl`.


## 0.2 (20.07.2019)

- Added [documentation](https://rafalp.github.io/async-caches/).
- Added code of conduct.
- Updated `cache.add` to return `True` if key was created in cache and `False` it it didn't.
- Updated `cache.get_or_set` to support callable for `default` value.
- Added value check for `timeout` that will raise `ValueError` if its set to `0`. Use `None` instead or don't explicitly pass the value to the argument.


## 0.1 (14.07.2019)

- Initial release of the library 🎉