from uuid import uuid4

import pytest
from fastagency.ui.console import ConsoleUI

from my_fastagency_app_without_auth.workflow import wf
from tests.conftest import InputMock


def test_workflow(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([""] * 5))

    result = wf.run(
        name="simple_learning",
        ui=ConsoleUI().create_workflow_ui(workflow_uuid=uuid4().hex),
    )

    assert result is not None
