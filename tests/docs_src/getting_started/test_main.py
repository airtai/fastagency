import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Help me learn a maths problem for 3rd grade"


@pytest.mark.openai
def test_cli_with_security(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app, ["run", "docs/docs_src/tutorial/getting_started/main.py"]
    )
    assert INPUT_MESSAGE in result.stdout
    assert "Teacher_Agent -> Student_Agent" in result.stdout
