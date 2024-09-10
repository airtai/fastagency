import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Who is Leonardo da Vinci?"


@pytest.mark.skip("Not working")
@pytest.mark.openai
@pytest.mark.parametrize(
    ("input_message", "path"), [("Who is Leonardo da Vinci?", "examples/cli/main.py ")]
)
def test_cli(monkeypatch: pytest.MonkeyPatch, input_message: str, path: str) -> None:
    monkeypatch.setattr("builtins.input", InputMock([input_message]))

    result = runner.invoke(app, ["run", path], color=True)

    assert INPUT_MESSAGE in result.stdout
    assert "workflow_completed" in result.stdout
