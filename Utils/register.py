from typing import Union
from warnings import warn

def load_from_cfg(obj:object, cfg:Union[dict, object]):
    """Load a config to the object, every key and value will be inserted into the target object.

    Args:
        obj (object): Target object.
        cfg (Union[dict, object]): Config.
    """
    if isinstance(cfg, object):
        keys = [x for x in dir(cfg) if not x.startswith("__")]
        for k in keys:
            if hasattr(obj, k):
                warn(f"{type(obj).__name__} already have the key of {k}.")
            setattr(obj, k, getattr(cfg, k))
    else:
        for k,v in cfg.items():
            if hasattr(obj, k):
                warn(f"{type(obj).__name__} already have the key of {k}.")
            setattr(obj, k, v)

