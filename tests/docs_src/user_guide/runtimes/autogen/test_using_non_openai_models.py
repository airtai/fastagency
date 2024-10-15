import pytest
from typer.testing import CliRunner

from fastagency.cli import app

from .....conftest import InputMock
from ....helpers import skip_internal_server_error

runner = CliRunner()

INPUT_MESSAGE = "Get me daily forecast for Zagreb city"


@pytest.mark.openai
@skip_internal_server_error
def test_cli_together_ai(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app,
        [
            "run",
            "docs/docs_src/user_guide/runtimes/autogen/using_non_openai_models.py",
            "--single-run",
        ],
    )
    assert result.exit_code == 0
    assert INPUT_MESSAGE in result.stdout
    assert "get_daily_weather_daily_get" in result.stdout
