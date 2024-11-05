from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastagency.ui.console import ConsoleUI

from .workflow import wf


class InputMock:
    def __init__(self, responses: list[str]) -> None:
        """Initialize the InputMock."""
        self.responses = responses
        self.mock = MagicMock()

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        self.mock(*args, **kwargs)
        return self.responses.pop(0)


def test_workflow(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([""] * 5))

    result = wf.run(
        name="simple_learning",
        ui=ConsoleUI().create_workflow_ui(workflow_uuid=uuid4().hex),
    )

    assert result is not None
