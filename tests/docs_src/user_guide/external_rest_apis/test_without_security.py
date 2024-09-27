import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Get me daily forecast for Zagreb city"


@pytest.mark.openai
@pytest.mark.xfail(strict=False)
def test_cli_without_security(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app,
        ["run", "docs/docs_src/user_guide/external_rest_apis/main.py", "--single-run"],
    )
    assert result.exit_code == 0
    assert INPUT_MESSAGE in result.stdout
    assert "get_daily_weather_daily_get" in result.stdout
