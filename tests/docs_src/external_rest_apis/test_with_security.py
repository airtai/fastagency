import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from fastagency.core.io.console import ConsoleIO
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Get me hourly forecast for Zagreb city"


@pytest.mark.openai
def test_wf_with_security(monkeypatch: pytest.MonkeyPatch) -> None:
    from docs.docs_src.tutorial.external_rest_apis.security import wf

    monkeypatch.setattr("builtins.input", InputMock([""] * 5))

    result = wf.run(
        name="simple_weather_with_security",
        session_id="session_id",
        io=ConsoleIO(),
        initial_message=INPUT_MESSAGE,
    )

    assert result is not None


@pytest.mark.openai
def test_cli_with_security(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app, ["run", "docs/docs_src/tutorial/external_rest_apis/security.py"]
    )
    assert INPUT_MESSAGE in result.stdout
    assert "get_hourly_weather_hourly_get" in result.stdout
