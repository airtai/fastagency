import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Who is Leonardo da Vinci?"


@pytest.mark.openai
@pytest.mark.parametrize(
    ("input_message", "path"),
    [
        ("What is triangle inequality?", "examples/cli/main_console.py"),
        # ("What is the weather in London?", "examples/cli/main_user_proxy.py"),
    ],
)
def test_cli(monkeypatch: pytest.MonkeyPatch, input_message: str, path: str) -> None:
    monkeypatch.setattr("builtins.input", InputMock([input_message] + [] * 10))

    result = runner.invoke(app, ["run", "--single-run", path], color=True)

    assert result.exit_code == 0, result
    assert input_message in result.stdout
    assert "workflow_completed" in result.stdout
