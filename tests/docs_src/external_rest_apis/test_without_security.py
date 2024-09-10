import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from fastagency.core.io.console import ConsoleIO
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Get me daily forecast for Zagreb city"


@pytest.mark.openai
def test_wf_without_security(monkeypatch: pytest.MonkeyPatch) -> None:
    from docs.docs_src.tutorial.external_rest_apis.main import wf

    monkeypatch.setattr("builtins.input", InputMock([""] * 5))

    result = wf.run(
        name="simple_weather",
        session_id="session_id",
        io=ConsoleIO(),
        initial_message=INPUT_MESSAGE,
    )

    assert result is not None


@pytest.mark.openai
def test_cli_without_security(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", InputMock([INPUT_MESSAGE]))

    result = runner.invoke(
        app, ["run", "docs/docs_src/tutorial/external_rest_apis/main.py"]
    )
    assert INPUT_MESSAGE in result.stdout
    assert "get_daily_weather_daily_get" in result.stdout
