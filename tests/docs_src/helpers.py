import functools
from typing import Any, Callable, TypeVar

import pytest

from fastagency.logging import get_logger

__all__ = ["skip_internal_server_error"]

logger = get_logger(__file__)

C = TypeVar("C", bound=Callable[..., Any])


def skip_internal_server_error(func: C) -> C:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"skip_internal_server_error(): error detected: {e}")
            logger.info(
                f"skip_internal_server_error(): e.args[0]            : {e.args[0]}"
            )
            if (
                "InternalServerError" in e.args[0]
                and "The model produced invalid content. Consider modifying your prompt if you are seeing this error persistently."
                in e.args[0]
            ):
                logger.warning(
                    "skip_internal_server_error(): Internal server error detected, marking the test as XFAIL"
                )
                pytest.xfail("Internal server error detected")
            logger.error(f"skip_internal_server_error(): reraising: {e}")
            raise

    return wrapper  # type: ignore[return-value]
