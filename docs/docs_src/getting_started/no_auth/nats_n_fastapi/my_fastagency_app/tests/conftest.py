from typing import Any
from unittest.mock import MagicMock


class InputMock:
    def __init__(self, responses: list[str]) -> None:
        """Initialize the InputMock."""
        self.responses = responses
        self.mock = MagicMock()

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        self.mock(*args, **kwargs)
        return self.responses.pop(0)
