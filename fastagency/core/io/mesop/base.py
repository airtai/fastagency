from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from ...base import (
    AskingMessage,
    IOMessage,
    IOMessageVisitor,
    Runnable,
)


class Mesop(IOMessageVisitor):  # Chatable
    def __init__(
        self,
        super_conversation: Optional["Mesop"] = None,
        *,
        port: Optional[int] = None,
    ) -> None:
        """Initialize the console IO object.

        Args:
            super_conversation (Optional[Mesop], optional): The super conversation. Defaults to None.
            port (Optional[int], optional): The port to use for the conversation. Defaults to None.
        """
        self.super_conversation: Optional[Mesop] = super_conversation
        self.sub_conversations: list[Mesop] = []

    @contextmanager
    def start(self, app: Runnable) -> Generator[None, None, None]:
        yield

    def visit_default(self, message: IOMessage) -> None:
        print("-" * 80)  # noqa: T201 `print` found
        print("asdict(message)")  # noqa: T201 `print` found

        if isinstance(message, AskingMessage):
            input()

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)

    def create_subconversation(self) -> "Mesop":
        sub_conversation = Mesop(self)
        self.sub_conversations.append(sub_conversation)

        return sub_conversation

    @property
    def main_path(self) -> str:
        return (Path(__file__).parent / "main.py").absolute().as_posix()
