import os
import subprocess  # nosec: B404
import sys
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

    def create(self, app: Runnable, import_string: str) -> None:
        pass

    def start(
        self,
        app: Runnable,
        import_string: str,
        name: Optional[str] = None,
        initial_message: Optional[str] = None,
    ) -> None:
        env = os.environ.copy()
        env["IMPORT_STRING"] = import_string
        process = subprocess.Popen(  # nosec: B603, B607
            ["mesop", self.main_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )
        try:
            # Print stdout line by line
            for line in process.stdout:  # type: ignore[union-attr]
                print(line, end="")  # noqa: T201 `print` found

            # Print stderr line by line
            for line in process.stderr:  # type: ignore[union-attr]
                print(line, end="", file=sys.stderr)  # noqa: T201 `print` found

        finally:
            process.terminate()

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
