import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

from ..helpers import skip_internal_server_error

runner = CliRunner()

INPUT_MESSAGE = "Who is Pitagora?"


@pytest.mark.openai
@skip_internal_server_error
def test_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app,
        [
            "run",
            "docs/docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/local/main_console.py",
            "--single-run",
        ],
    )

    assert result.exit_code == 0
    assert INPUT_MESSAGE in result.stdout
    assert "Teacher_Agent (to Student_Agent)" in result.stdout
