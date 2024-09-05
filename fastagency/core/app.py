__all__ = ["FastAgency"]

import textwrap
from typing import Optional

from .base import Chatable, SystemMessage, TextInput, WorkflowCompleted, Workflows


class FastAgency:
    def __init__(self, wf: Workflows, io: Chatable) -> None:
        """Initialize the FastAgency object.

        Args:
            wf (Workflows): The workflows object to use
            io (Chatable): The IO object to use
        """
        self.wf = wf
        self.io = io

    def run(self, name: Optional[str], initial_message: Optional[str] = None) -> None:
        """Run a workflow.

        Args:
            name (Optional[str]): The name of the workflow to run. If not provided, the default workflow will be run.
            initial_message (Optional[str], optional): The initial message to send to the workflow. If not provided, a default message will be sent. Defaults to None.
        """
        while True:
            name = self.wf.names[0] if name is None else name
            description = self.wf.get_description(name)

            if initial_message is None:
                initial_message = self.io.process_message(
                    TextInput(
                        sender="FastAgency",
                        recepient="user",
                        prompt=(
                            f"Starting a new workflow '{name}' with the following description:"
                            + "\n\n"
                            + f"{description}"
                            + "\n\nPlease enter an initial message"
                        ),
                    )
                )
            else:
                self.io.process_message(
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

            result = self.wf.run(
                name=name,
                session_id="session_id",
                io=self.io.create_subconversation(),
                initial_message="Hi!" if initial_message is None else initial_message,
            )

            self.io.process_message(
                WorkflowCompleted(
                    sender="workflow",
                    recepient="user",
                    result=result,
                )
            )

            initial_message = None
