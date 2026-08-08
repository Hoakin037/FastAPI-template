import typing
from collections.abc import Callable
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any

if typing.TYPE_CHECKING:
    import logging


def logg_function(func: Callable, description: str) -> Callable:
    is_coroutine = iscoroutinefunction(func)

    if is_coroutine:

        @wraps(func)
        async def async_wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
            logger: logging.Logger | None = getattr(instance, "logger", None)

            if logger:
                logger.debug(" <--> %s() called. %s", func.__name__, description)

            result = await func(instance, *args, **kwargs)
            if logger:
                logger.debug(" <--> %s() finished.", func.__name__)

            return result

        return async_wrapper

    @wraps(func)
    def sync_wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
        logger: logging.Logger | None = getattr(instance, "logger", None)

        if logger:
            logger.debug(" <--> %s() called. %s", func.__name__, description)

        result = func(instance, *args, **kwargs)
        if logger:
            logger.debug(" <--> %s() finished.", func.__name__)

        return result

    return sync_wrapper
