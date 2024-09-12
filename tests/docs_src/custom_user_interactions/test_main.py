import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Get me mock english exam questions for 5th grade"


@pytest.mark.openai
def test_cli_with_security(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app, ["run", "docs/docs_src/tutorial/custom_user_interactions/main.py"]
    )
    assert INPUT_MESSAGE in result.stdout
    assert "retrieve_exam_questions" in result.stdout
