from typing import Any, Collection, Dict, Union

# Note: "Any" should be "Serializable"
# See https://github.com/python/mypy/issues/7069
Serializable = Union[bool, float, int, str, Collection[Any], Dict[str, Any]]
Version = Union[int, str]
