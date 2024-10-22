__all__ = ["FastAgency"]

from collections.abc import Awaitable, Generator
from contextlib import contextmanager
from typing import Any, Callable, Optional, Union

from .base import (
    ASGIProtocol,
    ProviderProtocol,
    Runnable,
    UIBase,
    WSGIProtocol,
)
from .exceptions import (
    FastAgencyASGINotImplementedError,
    FastAgencyWSGINotImplementedError,
)
from .logging import get_logger

logger = get_logger(__name__)


class FastAgency:  # Runnable
    def __init__(
        self,
        provider: ProviderProtocol,
        ui: UIBase,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """Initialize the FastAgency object.

        Args:
            provider (ProviderProtocol): The provider object to use
            ui (UI): The UI object to use
            title (Optional[str], optional): The title of the FastAgency. If None, the default string will be used. Defaults to None.
            description (Optional[str], optional): The description of the FastAgency. If None, the default string will be used. Defaults to None.
        """
        _self: Runnable = self
        self._title = title or "FastAgency application"
        self._description = description or "FastAgency application"

        logger.info(
            f"Initializing FastAgency {self} with workflows: {provider} and UI: {ui}"
        )
        self._provider = provider
        self._ui = ui
        logger.info(f"Initialized FastAgency: {self}")

    @property
    def title(self) -> str:
        """Return the title of the FastAgency."""
        return self._title

    @property
    def description(self) -> str:
        """Return the description of the FastAgency."""
        return self._description

    def __str__(self) -> str:
        """Return the string representation of the FastAgency."""
        return f"<FastAgency title={self._title}>"

    @property
    def provider(self) -> ProviderProtocol:
        """Return the provider object."""
        return self._provider

    @property
    def ui(self) -> UIBase:
        """Return the UI object."""
        return self._ui

    @contextmanager
    def create(self, import_string: str) -> Generator[None, None, None]:
        """Create the FastAgency."""
        with self._ui.create(app=self, import_string=import_string):
            yield

    def start(
        self,
        *,
        import_string: str,
        name: Optional[str] = None,
        params: dict[str, Any],
        single_run: bool = False,
    ) -> None:
        """Start the FastAgency."""
        self.ui.start(
            app=self,
            import_string=import_string,
            name=name,
            params=params,
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
        logger.debug(f"Handling WSGI request: {environ}")
        if isinstance(self.ui, WSGIProtocol):
            return self.ui.handle_wsgi(self, environ, start_response)
        else:
            raise FastAgencyWSGINotImplementedError(
                f"WSGI interface not supported for UI: {self.ui.__class__.__name__}. Try running with 'fastapi run' or with a ASGI server like 'uvicorn'."
            )

    async def handle_asgi(
        self,
        scope: dict[str, Any],
        receive: Callable[[dict[str, Any]], Awaitable[None]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if isinstance(self.ui, ASGIProtocol):
            return await self.ui.handle_asgi(self, scope, receive, send)
        else:
            raise FastAgencyASGINotImplementedError(
                f"ASGI interface not supported for UI: {self.ui.__class__.__name__}. Try running with 'fastapi run' or with a WSGI server like 'gunicorn'/'waitress'."
            )
