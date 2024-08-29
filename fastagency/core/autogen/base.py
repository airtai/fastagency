import logging
import re
from typing import Any, Callable, Dict, List, Tuple

from autogen.io import IOStream

from ..base import ChatMessage, Chatable, Workflow, Workflows

__all__ = [
    "IOStreamAdapter",
    "AutoGenWorkflows",
]


# Get the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a stream handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


class IOStreamAdapter:  # IOStream
    def __init__(self, io: Chatable) -> None:
        """Initialize the adapter with a ChatableIO object.

        Args:
            io (ChatableIO): The ChatableIO object to adapt

        """
        self.io = io
        self.current_message = ChatMessage(
            sender=None, recepient=None, heading=None, body=None
        )
        self.messages: List[ChatMessage] = []

    def _process_message(self, body: str) -> bool:
        logger.info(f"Processing message: {body=}, {self.current_message=}")

        # the end of the message
        if (
            body
            == "\n--------------------------------------------------------------------------------\n"
        ):
            self.messages.append(self.current_message)
            self.current_message = ChatMessage(
                sender=None, recepient=None, heading=None, body=None
            )
            return True

        # match parts of the message
        if body == "\x1b[31m\n>>>>>>>> USING AUTO REPLY...\x1b[0m\n":
            self.current_message.heading = "AUTO REPLY"
        elif re.match(
            "^\\x1b\\[33m([a-zA-Z0-9_-]+)\\x1b\\[0m \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
            body,
        ):
            sender, recepient = re.findall(
                "^\\x1b\\[33m([a-zA-Z0-9_-]+)\\x1b\\[0m \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
                body,
            )[0]
            self.current_message.sender = sender
            self.current_message.recepient = recepient
        elif re.match(
            "^\\x1b\\[32m\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
            body,
        ):
            call_id, function_name = re.findall(
                "^\\x1b\\[32m\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
                body,
            )[0]
            self.current_message.heading = (
                f"SUGGESTED TOOL CALL ({call_id}): {function_name}"
            )
        elif re.match("\\x1b\\[32m(\\*+)\\x1b\\[0m\n", body):
            pass
        elif re.match(
            "^\\x1b\\[35m\\n>>>>>>>> EXECUTING FUNCTION ([a-zA-Z_]+)...\\x1b\\[0m\\n$",
            body,
        ):
            function_name = re.findall(
                "^\\x1b\\[35m\\n>>>>>>>> EXECUTING FUNCTION ([a-zA-Z_]+)...\\x1b\\[0m\\n$",
                body,
            )[0]
            self.current_message.heading = f"EXECUTING FUNCTION {function_name}"
        elif re.match(
            "^\\x1b\\[32m\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
            body,
        ):
            call_id = re.findall(
                "^\\x1b\\[32m\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
                body,
            )[0]
            self.current_message.heading = f"RESPONSE FROM CALLING TOOL ({call_id})"
        else:
            body = (
                self.current_message.body if self.current_message.body else ""
            ) + body
            self.current_message.body = body

        return False

    def print(
        self, *objects: Any, sep: str = " ", end: str = "\n", flush: bool = False
    ) -> None:
        body = sep.join(map(str, objects)) + end
        ready_to_send = self._process_message(body)
        if ready_to_send:
            message = self.messages[-1]
            self.io.print(message)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        message = ChatMessage(sender=None, recepient=None, heading=None, body=prompt)
        return self.io.input(message, password=password)


class AutoGenWorkflows(Workflows):
    def __init__(self) -> None:
        """Initialize the workflows."""
        self._workflows: Dict[str, Tuple[Callable[[Chatable, str, str], str], str]] = {}

    def register(
        self, name: str, description: str, *, fail_on_redefintion: bool = False
    ) -> Callable[[Workflow], Workflow]:
        def decorator(func: Workflow) -> Workflow:
            if name in self._workflows:
                if fail_on_redefintion:
                    raise ValueError(f"A workflow with name '{name}' already exists.")
                else:
                    logger.warning(f"Overwriting workflow with name '{name}'")

            self._workflows[name] = func, description
            return func

        return decorator

    def run(
        self, name: str, session_id: str, io: Chatable, initial_message: str
    ) -> str:
        workflow, description = self._workflows[name]

        iostream = IOStreamAdapter(io)

        with IOStream.set_default(iostream):
            return workflow(io, initial_message, session_id)
