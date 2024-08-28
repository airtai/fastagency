from dataclasses import dataclass
from typing import Callable, List, Optional, Protocol, TypeVar, runtime_checkable

__all__ = [
    "ChatMessage",
    "MultipleChoice",
    "Chatable",
    "Workflow",
    "Workflows",
]


@dataclass
class ChatMessage:
    sender: Optional[str]
    recepient: Optional[str]
    heading: Optional[str]
    body: Optional[str]


@dataclass
class MultipleChoice:
    message: ChatMessage
    choices: List[str]
    default: Optional[str] = None
    single: bool = True


@runtime_checkable
class Chatable(Protocol):
    def input(self, message: ChatMessage, *, password: bool = False) -> str: ...

    def print(self, message: ChatMessage) -> None: ...

    def select(self, choice: MultipleChoice) -> str: ...

    def create_subconversation(self) -> "Chatable": ...


Workflow = TypeVar("Workflow", bound=Callable[[Chatable, str, str], str])


@runtime_checkable
class Workflows(Protocol):
    def register(
        self, name: str, description: str
    ) -> Callable[[Workflow], Workflow]: ...

    def run(
        self, name: str, session_id: str, io: Chatable, initial_message: str
    ) -> str: ...
