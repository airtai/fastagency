import getpass
import json
import textwrap
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional

from ...base import (
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    Runnable,
    TextInput,
    TextMessage,
    run_workflow,
)
from ...logging import get_logger

logger = get_logger(__name__)


class ConsoleUI(IOMessageVisitor):  # implements UI
    @dataclass
    class ConsoleMessage:
        """A console message."""

        sender: Optional[str]
        recipient: Optional[str]
        heading: Optional[str]
        body: Optional[str]

    def __init__(
        self,
        super_conversation: Optional["ConsoleUI"] = None,
    ) -> None:
        """Initialize the console UI object.

        Args:
            super_conversation (Optional[UI], optional): The super conversation. Defaults to None.
        """
        self.super_conversation: Optional[ConsoleUI] = super_conversation
        self.sub_conversations: list[ConsoleUI] = []

    @contextmanager
    def create(self, app: Runnable, import_string: str) -> Iterator[None]:
        yield

    def start(
        self,
        *,
        app: Runnable,
        import_string: str,
        name: Optional[str] = None,
        initial_message: Optional[str] = None,
        single_run: bool = False,
    ) -> None:
        run_workflow(
            wf=app.wf,
            ui=self,
            name=name,
            initial_message=initial_message,
            single_run=single_run,
        )

    @property
    def level(self) -> int:
        return (
            0 if self.super_conversation is None else self.super_conversation.level + 1
        )

    def _format_message(self, console_msg: ConsoleMessage) -> str:
        heading = f"[{console_msg.heading}]" if console_msg.heading else ""
        title = f"{console_msg.sender} -> {console_msg.recipient} {heading}"[:74]

        s = f"""╭─ {title} {'─' * (74 - len(title))}─╮
│
{textwrap.indent(textwrap.fill(console_msg.body if console_msg.body else '', replace_whitespace=False, drop_whitespace=False), '│ ', predicate=lambda line: True)}
╰{'─' * 78}╯
"""
        # remove empty lines
        s = "\n".join([line for line in s.split("\n") if line.strip()])

        # add trailing withespace and │ to each line except the first and the last
        lines = s.split("\n")
        s = (
            lines[0]
            + "\n"
            + "\n".join([line + " " * (79 - len(line)) + "│" for line in lines[1:-1]])
            + "\n"
            + lines[-1]
            + "\n"
        )

        return s

    def _indent(self, text: str) -> str:
        return textwrap.indent(text, " " * 4 * self.level)

    def _format_and_print(self, console_msg: ConsoleMessage) -> None:
        msg = self._format_message(console_msg)
        msg = self._indent(msg)

        print(msg)  # noqa: T201 `print` found

    def visit_default(self, message: IOMessage) -> None:
        content = message.model_dump()["content"]
        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recipient=message.recipient,
            heading=message.type,
            body=json.dumps(content, indent=2),
        )
        self._format_and_print(console_msg)

    def visit_text_message(self, message: TextMessage) -> None:
        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recipient=message.recipient,
            heading=message.type,
            body=message.body,
        )
        self._format_and_print(console_msg)

    def visit_text_input(self, message: TextInput) -> str:
        suggestions = (
            f" (suggestions: {', '.join(message.suggestions)})"
            if message.suggestions
            else ""
        )
        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recipient=message.recipient,
            heading=message.type,
            body=f"{message.prompt}{suggestions}:",
        )

        prompt = self._format_message(console_msg)
        prompt = self._indent(prompt)
        if message.password:
            return getpass.getpass(prompt)
        else:
            return input(prompt)

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recipient=message.recipient,
            heading=message.type,
            body=f"{message.prompt} (choices: {', '.join(message.choices)}, default: {message.default})",
        )

        prompt = self._format_message(console_msg)
        prompt = self._indent(prompt)
        while True:
            # logger.info(f"visit_multiple_choice(): {prompt=}")
            retval = input(prompt)
            if retval in message.choices:
                return retval
            elif retval == "" and message.default:
                return message.default
            else:
                print(f"Invalid choice ('{retval}'). Please try again.")  # noqa: T201 `print` found

    def process_message(self, message: IOMessage) -> Optional[str]:
        # logger.info(f"process_message(): {message=}")
        return self.visit(message)

    # def process_streaming_message(self, message: IOStreamingMessage) -> str | None:
    #     raise NotImplementedError

    def create_subconversation(self) -> "ConsoleUI":
        sub_conversation = ConsoleUI(self)
        self.sub_conversations.append(sub_conversation)

        return sub_conversation
