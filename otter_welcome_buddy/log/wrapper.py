import logging
from functools import wraps
from typing import Any, Callable, Optional


def log_function(level: int = logging.INFO, message: Optional[str] = None) -> Callable:
    """Decorator to log that the function is being called"""

    def decorate(func: Callable) -> Callable:
        logmsg = message if message else func.__module__ + "." + func.__name__

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            # We need to create proper class to init Logger instead of setting log level
            logging.getLogger().setLevel(logging.INFO)
            logging.log(level, logmsg)
            return func(*args, **kwargs)

        return wrapper

    return decorate
