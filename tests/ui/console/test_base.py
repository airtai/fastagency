from collections.abc import Iterator
from typing import Any

import pytest

from fastagency.app import FastAgency
from fastagency.base import UI
from fastagency.runtimes.ag2 import AutoGenWorkflows
from fastagency.ui.console import ConsoleUI


@pytest.fixture
def import_string() -> str:
    return "main:app"


@pytest.fixture
def app(import_string: str) -> Iterator[FastAgency]:
    wf = AutoGenWorkflows()
    console = ConsoleUI()
    app = FastAgency(provider=wf, ui=console)

    @wf.register(name="noop", description="No operation")
    def noop(ui: UI, params: dict[str, Any]) -> str:
        return "ok"

    try:
        with app.create(import_string):
            yield app
    finally:
        # todo: close the app
        pass


class TestConsoleUIInput:
    def test_app_create_n_start(
        self, import_string: str, app: FastAgency, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "whatsapp")
        app.start(import_string=import_string, single_run=True, params={})
        assert isinstance(app, FastAgency)
        assert isinstance(app.ui, ConsoleUI)
