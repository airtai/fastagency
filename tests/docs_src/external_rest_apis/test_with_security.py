import pytest

from fastagency.core.io.console import ConsoleIO
from tests.conftest import InputMock


@pytest.mark.openai
def test_without_security(monkeypatch: pytest.MonkeyPatch) -> None:
    from docs.docs_src.tutorial.external_rest_apis.security import wf

    monkeypatch.setattr("builtins.input", InputMock([""] * 5))

    initial_message = "Get me hourly forecast for Zagreb city"
    result = wf.run(
        name="simple_weather_with_security",
        session_id="session_id",
        io=ConsoleIO(),
        initial_message=initial_message,
    )

    assert result is not None
