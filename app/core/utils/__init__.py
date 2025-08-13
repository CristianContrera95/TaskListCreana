from enum import Enum


def apply_filter(value: str, filter_: list | None) -> bool:
    if filter_ is None or (isinstance(filter_, list) and len(filter_) == 0):
        return True
    for f in filter_:
        if isinstance(f, str) and value == f:
            return True
        if isinstance(f, Enum) and value in f.value:
            return True
    return False
