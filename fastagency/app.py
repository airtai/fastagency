__all__ = ["FastAgency"]

from collections.abc import Awaitable, Generator
from contextlib import contextmanager
from typing import Any, Callable, Optional, Union

from .base import ASGI, UI, WSGI, Workflows
from .exceptions import (
    FastAgencyASGINotImplementedError,
    FastAgencyWSGINotImplementedError,
)


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

    def __call__(self, *args: Any) -> Union[Awaitable[None], list[bytes]]:
        if len(args) == 2 and callable(args[1]):
            # WSGI interface
            environ, start_response = args
            return self.handle_wsgi(environ, start_response)
        elif len(args) == 3 and callable(args[1]) and callable(args[2]):
            # ASGI interface
            scope, receive, send = args
            scope_type = scope.get("type")
            if scope_type == "http":
                return self.handle_asgi(scope, receive, send)
            else:
                raise NotImplementedError(
                    f"ASGI scope type '{scope_type}' not supported."
                )
        else:
            raise TypeError(f"Invalid arguments for __call__: {args}")

    def handle_wsgi(
        self, environ: dict[str, Any], start_response: Callable[..., Any]
    ) -> list[bytes]:
        if isinstance(self.ui, WSGI):
            return self.ui.handle_wsgi(self, environ, start_response)
        else:
            raise FastAgencyWSGINotImplementedError(
                "WSGI interface not supported for UI: {self.ui}"
            )

    async def handle_asgi(
        self,
        scope: dict[str, Any],
        receive: Callable[[dict[str, Any]], Awaitable[None]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if isinstance(self.ui, ASGI):
            return await self.ui.handle_asgi(self, scope, receive, send)
        else:
            raise FastAgencyASGINotImplementedError(
                "ASGI interface not supported for UI: {self.ui}"
            )
