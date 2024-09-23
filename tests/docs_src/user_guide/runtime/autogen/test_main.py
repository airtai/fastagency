import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "What's the weather in Zagreb'?"


@pytest.mark.openai
def test_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app, ["run", "docs/docs_src/user_guide/runtime/autogen/main.py", "--single-run"]
    )
    assert result.exit_code == 0
    assert INPUT_MESSAGE in result.stdout
    assert "workflow -> user [workflow_completed]" in result.stdout