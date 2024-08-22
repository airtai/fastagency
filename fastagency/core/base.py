import getpass
from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable


@dataclass
class ChatMessage:
    sender: Optional[str]
    recepient: Optional[str]
    heading: Optional[str]
    body: Optional[str]


@runtime_checkable
class ChatableIO(Protocol):
    def input(self, message: ChatMessage, *, password: bool = False) -> str: ...

    def print(self, message: ChatMessage) -> None: ...


class ConsoleIO(ChatableIO):
    def input(self, message: ChatMessage, *, password: bool = False) -> str:
        prompt = f"{message.sender} -> {message.recepient}:" + "\n" + f"{message.body}"
        if password:
            return getpass.getpass(prompt)
        else:
            return input(prompt)

    def print(self, message: ChatMessage) -> None:
        if message.sender is not None:
            print(  # noqa: T201 `print` found
                f"{message.sender} -> {message.recepient}:" + "\n" + f"{message.body}"
            )
        else:
            print(message.body)  # noqa: T201 `print` found


@runtime_checkable
class Chatable(Protocol):
    def init_chat(self, message: str) -> None: ...

    def continue_chat(self, message: str) -> None: ...


@runtime_checkable
class ChatableFactory(Protocol):
    def create(self, session_id: str) -> Chatable: ...
