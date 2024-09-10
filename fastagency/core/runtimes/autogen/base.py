import json
import re
from dataclasses import asdict, dataclass
from typing import Any, Callable, Optional

from autogen.io import IOStream

from ....logging import get_logger
from ...base import (
    AskingMessage,
    Chatable,
    IOMessage,
    MessageType,
    MultipleChoice,
    TextInput,
    Workflow,
    Workflows,
)

__all__ = [
    "AutoGenWorkflows",
    "IOStreamAdapter",
]


# Get the logger
logger = get_logger(__name__)

logger.info("Importing autogen.base.py")

_patterns = {
    "end_of_message": "^\\n--------------------------------------------------------------------------------\\n$",
    "auto_reply": "^\\x1b\\[31m\\n>>>>>>>> USING AUTO REPLY...\\x1b\\[0m\\n$",
    "sender_recipient": "^\\x1b\\[33m([a-zA-Z0-9_-]+)\\x1b\\[0m \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
    "suggested_function_call": "^\\x1b\\[32m\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
    "stars": "\\x1b\\[32m(\\*+)\\x1b\\[0m\n",
    "function_call_execution": "^\\x1b\\[35m\\n>>>>>>>> EXECUTING FUNCTION ([a-zA-Z_]+)...\\x1b\\[0m\\n$",
    "response_from_calling_tool": "^\\x1b\\[32m\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
    "no_human_input_received": "^\\x1b\\[31m\\n>>>>>>>> NO HUMAN INPUT RECEIVED\\.\\x1b\\[0m$",
    "user_interrupted": "^USER INTERRUPTED\\n$",
    "arguments": "^Arguments: \\n(.*)\\n$",
    "auto_reply_input": "^Replying as ([a-zA-Z0-9_]+). Provide feedback to ([a-zA-Z0-9_]+). Press enter to skip and use auto-reply, or type 'exit' to end the conversation: $",
}


def _match(key: str, string: str, /) -> Optional[re.Match[str]]:
    pattern = _patterns[key]
    return re.match(pattern, string)


def _findall(key: str, string: str, /) -> tuple[str, ...]:
    pattern = _patterns[key]
    return re.findall(pattern, string)[0]  # type: ignore[no-any-return]


@dataclass
class CurrentMessage:
    sender: Optional[str] = None
    recipient: Optional[str] = None
    type: MessageType = "text_message"
    auto_reply: bool = False
    body: Optional[str] = None
    call_id: Optional[str] = None
    function_name: Optional[str] = None
    arguments: Optional[dict[str, Any]] = None
    retval: Optional[Any] = None

    def process_chunk(self, chunk: str) -> bool:  # noqa: C901
        # logger.info(f"CurrentMessage.process_chunk({chunk=}):")
        if _match("end_of_message", chunk):
            return True

        if _match("auto_reply", chunk):
            # logger.info("CurrentMessage.process_chunk(): auto_reply detected")
            self.auto_reply = True
        elif _match("sender_recipient", chunk):
            # logger.info("CurrentMessage.process_chunk(): sender_recipient detected")
            self.sender, self.recipient = _findall("sender_recipient", chunk)
        elif _match("suggested_function_call", chunk):
            # logger.info("CurrentMessage.process_chunk(): suggested_function_call detected")
            self.call_id, self.function_name = _findall(
                "suggested_function_call", chunk
            )
            self.type = "suggested_function_call"
        elif _match("stars", chunk):
            # logger.info("CurrentMessage.process_chunk(): stars detected")
            pass
        elif _match("function_call_execution", chunk):
            # logger.info("CurrentMessage.process_chunk(): function_call_execution detected")
            self.function_name = _findall("function_call_execution", chunk)  # type: ignore[assignment]
            self.type = "function_call_execution"
        elif _match("response_from_calling_tool", chunk):
            # logger.info("CurrentMessage.process_chunk(): response_from_calling_tool detected")
            self.type = "function_call_execution"
            self.call_id = _findall("response_from_calling_tool", chunk)  # type: ignore[assignment]
        elif _match("no_human_input_received", chunk):
            # logger.info("CurrentMessage.process_chunk(): no_human_input_received detected")
            pass
        elif _match("user_interrupted", chunk):
            # logger.info("CurrentMessage.process_chunk(): user_interrupted detected")
            pass
        else:
            if self.type == "suggested_function_call":
                # logger.info("CurrentMessage.process_chunk(): parsing arguments")
                arguments_json: str = _findall("arguments", chunk)  # type: ignore[assignment]
                self.arguments = json.loads(arguments_json)
            elif self.type == "function_call_execution":
                # logger.info("CurrentMessage.process_chunk(): parsing retval")
                self.retval = chunk
            else:
                # logger.info("CurrentMessage.process_chunk(): parsing body")
                self.body = chunk if self.body is None else self.body + chunk

        return False

    def process_input(
        self, prompt: str, password: bool, messages: list[IOMessage]
    ) -> AskingMessage:
        last_message = messages[-1]
        sender, recipient = None, None
        message: AskingMessage

        if _match("auto_reply_input", prompt):
            logger.info("IOStreamAdapter.input(): auto_reply_input detected")
            sender, recipient = _findall("auto_reply_input", prompt)  # type: ignore[assignment]

        if last_message.type == "suggested_function_call":
            logger.info("IOStreamAdapter.input(): suggested_function_call detected")
            message = MultipleChoice(
                sender=sender,
                recipient=recipient,
                prompt="Please approve the suggested function call.",
                choices=["Approve", "Reject"],
                default="Approve",
            )
        else:
            logger.info("IOStreamAdapter.input(): text_message detected")
            message = TextInput(
                sender=None, recipient=None, prompt=prompt, password=password
            )

        return message

    def create_message(self) -> IOMessage:
        kwargs = {k: v for k, v in asdict(self).items() if v is not None}
        # logger.info(f"CurrentMessage.create_message(): {kwargs=}")
        return IOMessage.create(**kwargs)


class IOStreamAdapter:  # IOStream
    def __init__(self, io: Chatable) -> None:
        """Initialize the adapter with a ChatableIO object.

        Args:
            io (ChatableIO): The ChatableIO object to adapt

        """
        self.io = io
        self.current_message = CurrentMessage()

        self.messages: list[IOMessage] = []
        if not isinstance(self.io, Chatable):
            raise ValueError("The io object must be an instance of Chatable.")

    def _process_message_chunk(self, chunk: str) -> bool:
        if self.current_message.process_chunk(chunk):
            msg = self.current_message.create_message()
            self.messages.append(msg)
            self.current_message = CurrentMessage()

            return True
        else:
            return False

    def print(
        self, *objects: Any, sep: str = " ", end: str = "\n", flush: bool = False
    ) -> None:
        # logger.info(f"print(): {objects=}, {sep=}, {end=}, {flush=}")
        body = sep.join(map(str, objects)) + end
        ready_to_send = self._process_message_chunk(body)
        if ready_to_send:
            message = self.messages[-1]
            self.io.process_message(message)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        # logger.info(f"input(): {prompt=}, {password=}")
        message: AskingMessage = self.current_message.process_input(
            prompt, password, self.messages
        )

        retval: str = self.io.process_message(message)  # type: ignore[assignment]

        # in case of approving a suggested function call, we need to return an empty string to AutoGen
        if (
            message.type == "multiple_choice"
            and self.messages[-1].type == "suggested_function_call"
            and retval == "Approve"
        ):
            retval = ""

        logger.info(f"input(): {retval=}")
        return retval


class AutoGenWorkflows(Workflows):
    def __init__(self) -> None:
        """Initialize the workflows."""
        self._workflows: dict[str, tuple[Callable[[Chatable, str, str], str], str]] = {}

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

    @property
    def names(self) -> list[str]:
        return list(self._workflows.keys())

    def get_description(self, name: str) -> str:
        _, description = self._workflows.get(name, (None, "Description not available!"))
        return description
