import logging
import re
from typing import Any, Callable, Dict, Tuple

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
        current_message = ChatMessage(
            sender=None, recepient=None, heading=None, body=None
        )
        self.messages = [current_message]

    def _process_message(self, body: str, current_message: ChatMessage) -> bool:
        # logger.info(f"Processing message: {body=}, {current_message=}")

        # the end of the message
        if (
            body
            == "\n--------------------------------------------------------------------------------\n"
        ):
            return True

        # match parts of the message
        if body == "\x1b[31m\n>>>>>>>> USING AUTO REPLY...\x1b[0m\n":
            current_message.heading = "AUTO REPLY"
        elif re.match(
            "^\\x1b\\[33m([a-zA-Z0-9_-]+)\\x1b\\[0m \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
            body,
        ):
            sender, recepient = re.findall(
                "^\\x1b\\[33m([a-zA-Z0-9_-]+)\\x1b\\[0m \\(to ([a-zA-Z0-9_-]+)\\):\\n\\n$",
                body,
            )[0]
            current_message.sender = sender
            current_message.recepient = recepient
        elif re.match(
            "^\\x1b\\[32m\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
            body,
        ):
            call_id, function_name = re.findall(
                "^\\x1b\\[32m\\*\\*\\*\\*\\* Suggested tool call \\((call_[a-zA-Z0-9]+)\\): ([a-zA-Z0-9_]+) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
                body,
            )[0]
            current_message.heading = (
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
            current_message.heading = f"EXECUTING FUNCTION {function_name}"
        elif re.match(
            "^\\x1b\\[32m\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
            body,
        ):
            call_id = re.findall(
                "^\\x1b\\[32m\\*\\*\\*\\*\\* Response from calling tool \\((call_[a-zA-Z0-9_]+)\\) \\*\\*\\*\\*\\*\\x1b\\[0m\\n$",
                body,
            )[0]
            current_message.heading = f"RESPONSE FROM CALLING TOOL ({call_id})"
        else:
            body = (current_message.body if current_message.body else "") + body
            current_message.body = body

        return False

    def print(
        self, *objects: Any, sep: str = " ", end: str = "\n", flush: bool = False
    ) -> None:
        current_message = self.messages[-1]
        body = sep.join(map(str, objects)) + end
        ready_to_send = self._process_message(body, current_message)
        if ready_to_send:
            self.io.print(current_message)
            self.messages.append(
                ChatMessage(sender=None, recepient=None, heading=None, body=None)
            )

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


# class AutoGenTeamChatable(Workflow):
#     def __init__(
#         self,
#         name: str,
#         initial_agent: ConversableAgent,
#         receiving_agent: ConversableAgent,
#         io: Chatable,
#     ) -> None:
#         """Initialize the team with a name.

#         Args:
#             name (str): The name of the team
#             initial_agent (ConversableAgent): The initial agent
#             receiving_agent (ConversableAgent): The receiving agent
#             io (ChatableIO): The ChatableIO object to use
#         """
#         self.name = name
#         self.initial_agent = initial_agent
#         self.receiving_agent = receiving_agent
#         self.io: Optional[Chatable] = io
#         self.iostream = IOStreamAdapter(self.io)

#     def init_chat(self, message: str, **kwargs: Any) -> str:
#         with IOStream.set_default(self.iostream):
#             chat_history = self.initial_agent.initiate_chat(
#                 self.receiving_agent,
#                 message=message,
#                 summary_method="last_msg",
#                 **kwargs,
#             )
#             return chat_history.summary  # type: ignore[no-any-return]

#     def continue_chat(self, message: str, **kwargs: Any) -> str:
#         with IOStream.set_default(self.iostream):
#             chat_history = self.initial_agent.initiate_chat(
#                 self.receiving_agent,
#                 message=message,
#                 clear_history=False,
#                 summary_method="last_msg",
#                 **kwargs,
#             )
#             return chat_history.summary  # type: ignore[no-any-return]


# class AutogenTeamAgents(TypedDict):
#     """A dictionary of agents for a team."""

#     initial_agent: ConversableAgent
#     receiving_agent: ConversableAgent


# AutoGenTeamFactory = TypeVar(
#     "AutoGenTeamFactory", bound=Callable[[], AutogenTeamAgents]
# )


# @dataclass
# class AutoGenContext:
#     ask_user_for_input: Callable[[str], str]


# class AutoGenTeam:
#     def __init__(
#         self,
#     ) -> None:
#         """Initialize the team with a name."""
#         self.factory_function: Optional[Callable[[], AutogenTeamAgents]] = None
#         self.name: Optional[str] = None
#         self.description: Optional[str] = None

#     def factory(
#         self, *, name: Optional[str], description: Optional[str]
#     ) -> Callable[[AutoGenTeamFactory], AutoGenTeamFactory]:
#         def inner(
#             factory_function: AutoGenTeamFactory,
#         ) -> AutoGenTeamFactory:
#             if self.factory_function is None:
#                 self.factory_function = factory_function
#                 self.name = name
#                 self.description = description
#             else:
#                 raise ValueError("Factory already set")

#             return factory_function

#         return inner

#     def create(self, session_id: str, io: Chatable) -> AutoGenTeamChatable:
#         name = f"{self.name}-{session_id}"
#         if self.factory_function is None:
#             raise ValueError("Factory not set")
#         agents = self.factory_function()
#         return AutoGenTeamChatable(
#             name,
#             initial_agent=agents["initial_agent"],
#             receiving_agent=agents["receiving_agent"],
#             io=io,
#         )
