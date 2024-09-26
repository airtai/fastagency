__all__ = ["FastAgency"]

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Awaitable, Callable, Optional

from .base import UI, Workflows


class FastAgency:  # Runnable
    def __init__(self, wf: Workflows, ui: UI) -> None:
        """Initialize the FastAgency object.

        Args:
            wf (Workflows): The workflows object to use
            ui (UI): The UI object to use
        """
        self._wf = wf
        self._ui = ui

    @property
    def wf(self) -> Workflows:
        """Return the workflows object."""
        return self._wf

    @property
    def ui(self) -> UI:
        """Return the UI object."""
        return self._ui

    @contextmanager
    def create(self, import_string: str) -> Generator[None, None, None]:
        """Create the FastAgency."""
        with self._ui.create(app=self, import_string=import_string):
            yield

    def start(
        self,
        import_string: str,
        name: Optional[str] = None,
        initial_message: Optional[str] = None,
        single_run: bool = False,
    ) -> None:
        """Start the FastAgency."""
        self.ui.start(
            app=self,
            import_string=import_string,
            name=name,
            initial_message=initial_message,
            single_run=single_run,
        )

    # # needed for uvicorn to recognize the class as a valid ASGI application
    # async def __call__(
    #     self,
    #     scope: dict[str, Any],
    #     receive: Callable[[], Awaitable[dict]],
    #     send: Callable[[dict], Awaitable[None]],
    # ) -> None:
    #     return await self.ui(scope, receive, send)

    def __call__(self, environ, start_response):
        self.ui.__class__._app = self
        return self.ui(environ, start_response)
        # # Define the HTTP response status and headers
        # status = '200 OK'
        # headers = [('Content-Type', 'text/plain')]
        # start_response(status, headers)

        # # Return the response body
        # response_body = b"Hello, this is MyApp!"
        # return [response_body]