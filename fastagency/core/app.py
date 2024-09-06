__all__ = ["FastAgency"]

from typing import Optional

from .base import Chatable, Workflows


class FastAgency:  # Runnable
    def __init__(self, wf: Workflows, io: Chatable) -> None:
        """Initialize the FastAgency object.

        Args:
            wf (Workflows): The workflows object to use
            io (Chatable): The IO object to use
        """
        self._wf = wf
        self._io = io

    @property
    def wf(self) -> Workflows:
        """Return the workflows object."""
        return self._wf

    @property
    def io(self) -> Chatable:
        """Return the IO object."""
        return self._io

    def create(self, import_string: str) -> None:
        """Create the FastAgency."""
        self._io.create(app=self, import_string=import_string)

    def start(
        self,
        import_string: str,
        name: Optional[str] = None,
        initial_message: Optional[str] = None,
    ) -> None:
        """Start the FastAgency."""
        self._io.start(
            app=self,
            import_string=import_string,
            name=name,
            initial_message=initial_message,
        )
