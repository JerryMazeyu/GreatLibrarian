from typing import List, Optional


def to_list(x) -> List:
    return x if isinstance(x, list) else [x]


def to_int(x) -> Optional[int]:
    try:
        result = int(x)
        return result
    except ValueError:
        return None
