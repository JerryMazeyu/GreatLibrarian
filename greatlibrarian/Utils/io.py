import os


def join(*x) -> str:
    """Join path.

    Args:
        x (str): paths

    Returns:
        str: Joined path
    """
    return os.path.join(*x)


def soft_mkdir(path, soft=True) -> bool:
    """Make direction if there is no file exists.

    Args:
        path (str): The path to create.
        verbose (bool, optional): If the path existed, if you want to ignore the error. Defaults to True.

    Returns:
        Bool: Success or not.
    """
    if os.path.exists(path):
        if not soft:
            raise ValueError(f"Path {path} has exits.")
        else:
            return False
    else:
        os.mkdir(path)
        return True
