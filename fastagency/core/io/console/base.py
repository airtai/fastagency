import getpass
import json
import textwrap
from dataclasses import dataclass
from typing import Optional

from ...base import IOMessage, IOMessageVisitor, MultipleChoice, TextInput, TextMessage


class ConsoleIO(IOMessageVisitor):  # Chatable
    @dataclass
    class ConsoleMessage:
        """A console message."""

        sender: Optional[str]
        recepient: Optional[str]
        heading: Optional[str]
        body: Optional[str]

    def __init__(self, super_conversation: Optional["ConsoleIO"] = None) -> None:
        """Initialize the console IO object.

        Args:
            super_conversation (Optional[Chatable], optional): The super conversation. Defaults to None.
        """
        self.super_conversation: Optional[ConsoleIO] = super_conversation
        self.sub_conversations: list[ConsoleIO] = []

    @property
    def level(self) -> int:
        return (
            0 if self.super_conversation is None else self.super_conversation.level + 1
        )

    def _format_message(self, console_msg: ConsoleMessage) -> str:
        heading = f"[{console_msg.heading}]" if console_msg.heading else ""
        title = f"{console_msg.sender} -> {console_msg.recepient} {heading}"[:74]

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
            recepient=message.recepient,
            heading=message.type,
            body=json.dumps(content, indent=2),
        )
        self._format_and_print(console_msg)

    def visit_text_message(self, message: TextMessage) -> None:
        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recepient=message.recepient,
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
            recepient=message.recepient,
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
            recepient=message.recepient,
            heading=message.type,
            body=f"{message.prompt} (choices: {', '.join(message.choices)}, default: {message.default})",
        )

        prompt = self._format_message(console_msg)
        prompt = self._indent(prompt)
        while True:
            retval = input(prompt)
            if retval in message.choices:
                return retval
            else:
                print(f"Invalid choice ('{retval}'). Please try again.")  # noqa: T201 `print` found

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)

    # def process_streaming_message(self, message: IOStreamingMessage) -> str | None:
    #     raise NotImplementedError

    def create_subconversation(self) -> "ConsoleIO":
        sub_conversation = ConsoleIO(self)
        self.sub_conversations.append(sub_conversation)

        return sub_conversation
