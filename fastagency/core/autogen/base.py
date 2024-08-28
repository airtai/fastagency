from typing import Any

from ..base import ChatMessage, Chatable

# __all__ = [
#     "IOStreamAdapter",
#     "AutoGenTeam",
#     "AutoGenTeamChatable",
#     "AutoGenTeamFactory",
#     "AutogenTeamAgents",
# ]


class IOStreamAdapter:  # IOStream
    def __init__(self, io: Chatable) -> None:
        """Initialize the adapter with a ChatableIO object.

        Args:
            io (ChatableIO): The ChatableIO object to adapt

        """
        self.io = io

    def print(
        self, *objects: Any, sep: str = " ", end: str = "\n", flush: bool = False
    ) -> None:
        body = sep.join(map(str, objects)) + end
        message = ChatMessage(sender=None, recepient=None, heading=None, body=body)
        self.io.print(message)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        message = ChatMessage(sender=None, recepient=None, heading=None, body=prompt)
        return self.io.input(message, password=password)


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
