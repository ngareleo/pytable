from typing import Any


def notNone(a: Any, b: Any):
    """Returns the value is not None. Returns a if both are not None."""
    return b if a is None else a


def cutAtSpace(w: str, width: int) -> tuple[str, str]:
    """Helper for trimming text for wrapping"""
    cut = w[:width]
    if cut == w:
        return (cut, "")
    exact_w = width - len(cut.split(" ")[-1])
    return (w[:exact_w], w[exact_w:])
