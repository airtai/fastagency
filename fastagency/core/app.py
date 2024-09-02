__all__ = ["FastAgency"]

from typing import Optional

from .base import Chatable, IOMessage, TextInput, Workflows


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

            if initial_message is None:
                initial_message = self.io.process_message(
                    TextInput(
                        sender="FastAgency",
                        recepient="user",
                        prompt="Please enter initial message:",
                    )
                )

            initial_message = (
                "Hi, I'm a user!" if initial_message is None else initial_message
            )

            self._run_workflow(name, initial_message)

            initial_message = None

    def _run_workflow(self, name: str, initial_message: str) -> None:
        self.io.process_message(
            IOMessage.create(
                sender="user",
                recepient="workflow",
                type="system_message",
                message={
                    "heading": f"Workflow {name} BEGIN",
                    "body": f"Starting workflow with initial_message: {initial_message}",
                },
            )
        )

        result = self.wf.run(
            name=name,
            session_id="session_id",
            io=self.io.create_subconversation(),
            initial_message=initial_message,
        )

        self.io.process_message(
            IOMessage.create(
                sender="user",
                recepient="workflow",
                type="system_message",
                message={
                    "heading": f"Workflow {name} END",
                    "body": f"Ending workflow with result: {result}",
                },
            )
        )
