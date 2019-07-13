from typing import Collection, Dict, Union

Serializable = Union[
    bool, float, int, str, Collection["Serializable"], Dict[str, "Serializable"]
]
Version = Union[int, str]
