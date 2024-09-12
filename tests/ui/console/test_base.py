from collections.abc import Iterator

import pytest

from fastagency.app import FastAgency
from fastagency.runtimes.autogen import AutoGenWorkflows
from fastagency.ui.console import ConsoleIO


@pytest.fixture
def app() -> Iterator[FastAgency]:
    wf = AutoGenWorkflows()
    console = ConsoleIO()
    app = FastAgency(wf=wf, io=console)

    try:
        import_string = "main:app"
        app.create(import_string)
        app.start(import_string)
        yield app
    finally:
        # todo: close the app
        pass


# class TestConsoleIOInput:
#     @pytest.skip("Not implemented")  # type: ignore[misc]
#     def test_user_proxy_auto_reply(self, app: FastAgency) -> None:
#         raise NotImplementedError
