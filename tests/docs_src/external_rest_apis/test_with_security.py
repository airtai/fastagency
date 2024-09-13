import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Get me hourly forecast for Zagreb city"


@pytest.mark.openai
def test_cli_with_security(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app, ["run", "docs/docs_src/user_guide/external_rest_apis/security.py"]
    )
    assert INPUT_MESSAGE in result.stdout
    assert "get_hourly_weather_hourly_get" in result.stdout
