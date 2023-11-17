def to_list(x):
    return x if isinstance(x, list) else [x]

def to_int(x):
    try:
        result = int(x)
        return result
    except ValueError:
        return None
