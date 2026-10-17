from collections.abc import Callable
from typing import Any


def is_dunder_method(func: Callable[[], Any]) -> bool:
    fn = func.__name__
    return fn.startswith("__") and fn.endswith("__")
