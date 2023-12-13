from typing import Any


def notNone(a: Any, b: Any):
    """Returns the value is not None. Returns a if both are not None."""
    return b if a is None else a
