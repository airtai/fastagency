import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Get me daily forecast for Zagreb city"


@pytest.mark.openai
def test_cli_without_security(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app, ["run", "docs/docs_src/tutorial/external_rest_apis/main.py"]
    )
    assert INPUT_MESSAGE in result.stdout
    assert "get_daily_weather_daily_get" in result.stdout
