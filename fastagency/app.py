__all__ = ["FastAgency"]

from collections.abc import Generator
from contextlib import contextmanager
from typing import Optional

from .base import UI, Workflows


class FastAgency:  # Runnable
    def __init__(self, wf: Workflows, ui: UI) -> None:
        """Initialize the FastAgency object.

        Args:
            wf (Workflows): The workflows object to use
            ui (Chatable): The UI object to use
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
    ) -> None:
        """Start the FastAgency."""
        self.ui.start(
            app=self,
            import_string=import_string,
            name=name,
            initial_message=initial_message,
        )
