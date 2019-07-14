# Async Caches

[![Build Status](https://travis-ci.org/rafalp/async-caches.svg?branch=master)](https://travis-ci.org/rafalp/async-caches)
[![Codecov](https://codecov.io/gh/rafalp/async-caches/branch/master/graph/badge.svg)](https://codecov.io/gh/rafalp/async-caches)

Caching library reimplementing [`django.core.cache` API](https://docs.djangoproject.com/en/2.2/topics/cache/#the-low-level-cache-api) with async support and type hints, inspired by [`encode/databases`](https://github.com/encode/databases).

Currently three cache backends are available:

* `dummy` - Dummy cache backend that doesn't cache anything. Used to disable caching in tests!
* `locmem` - Cache backend that stores data in thread's memory. Lets you develop and test caching without need to setup and maintin cache server.
* `redis` - Redis cache intended for use in actual deployments.

**Requirements:** Python 3.6+


## Installation

```console
$ pip install async-caches
```


## Credits and license

This is free software and you are welcome to modify and redistribute it under the conditions described in the license. For the complete license, refer to the LICENSE file.

Parts of software come from [databases](https://github.com/encode/databases/issues) package developed by Tom Christie and contributors and from [Django](https://github.com/django/django) package developed by Django project maintainers and contributors.