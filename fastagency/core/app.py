__all__ = ["FastAgency"]

import textwrap
from contextlib import contextmanager
from typing import Generator, Optional

from .base import Chatable, SystemMessage, TextInput, WorkflowCompleted, Workflows


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

    @contextmanager
    def start(self) -> Generator[None, None, None]:
        """Start the FastAgency."""
        with self._io.start(app=self):
            yield

    def run(self, name: Optional[str], initial_message: Optional[str] = None) -> None:
        """Run a workflow.

        Args:
            name (Optional[str]): The name of the workflow to run. If not provided, the default workflow will be run.
            initial_message (Optional[str], optional): The initial message to send to the workflow. If not provided, a default message will be sent. Defaults to None.
        """
        while True:
            name = self._wf.names[0] if name is None else name
            description = self._wf.get_description(name)

            if initial_message is None:
                initial_message = self._io.process_message(
                    TextInput(
                        sender="FastAgency",
                        recepient="user",
                        prompt=(
                            f"Starting a new workflow '{name}' with the following description:"
                            + "\n\n"
                            + f"{description}"
                            + "\n\nPlease enter an initial message:"
                        ),
                    )
                )
            else:
                self._io.process_message(
                    SystemMessage(
                        sender="FastAgency",
                        recepient="user",
                        message={
                            "body": (
                                f"Starting a new workflow '{name}' with the following description:"
                                + "\n\n"
                                + textwrap.indent(description, prefix=" " * 2)
                                + "\n\nand using the following initial message:"
                                + textwrap.indent(initial_message, prefix=" " * 2)
                            )
                        },
                    )
                )

            result = self._wf.run(
                name=name,
                session_id="session_id",
                io=self._io.create_subconversation(),
                initial_message="Hi!" if initial_message is None else initial_message,
            )

            self._io.process_message(
                WorkflowCompleted(
                    sender="workflow",
                    recepient="user",
                    result=result,
                )
            )

            initial_message = None
