from unittest.mock import ANY, MagicMock

import pytest
import requests
from typer.testing import CliRunner

from fastagency.cli import app

from .....conftest import InputMock
from ....helpers import skip_internal_server_error

runner = CliRunner()

INPUT_MESSAGE = "Send 'Hi!' to 123456789"


@pytest.mark.openai
@skip_internal_server_error
def test_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    mock = MagicMock()

    monkeypatch.setattr(requests, "post", mock)

    result = runner.invoke(
        app,
        [
            "run",
            "docs/docs_src/user_guide/runtimes/autogen/whatsapp.py",
            "--single-run",
        ],
    )

    mock.assert_called_with(
        "https://api.infobip.com/whatsapp/1/message/text",
        params={},
        json={
            "from": "447860099299",
            "to": "123456789",
            "content": {"text": "Hi!"},
            "messageId": ANY,
            "callbackData": "Callback data",
        },
        headers=ANY,
    )

    assert result.exit_code == 0
    assert "AutoGenWorkflows -> User [workflow_completed]" in result.stdout
