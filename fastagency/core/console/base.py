import getpass
import textwrap
from typing import List, Optional

from ..base import ChatMessage, Chatable, MultipleChoice


class ConsoleIO(Chatable):
    def __init__(self, super_conversation: Optional["ConsoleIO"] = None) -> None:
        """Initialize the console IO object.

        Args:
            super_conversation (Optional[Chatable], optional): The super conversation. Defaults to None.
        """
        self.super_conversation: Optional[ConsoleIO] = super_conversation
        self.sub_conversations: List[ConsoleIO] = []

    @property
    def level(self) -> int:
        return (
            0 if self.super_conversation is None else self.super_conversation.level + 1
        )

    def _format_message(self, message: ChatMessage) -> str:
        return f"""+{'-' * 80}+
|
| {message.sender} -> {message.recepient}: {message.heading if message.heading else ''}
|
{textwrap.indent(textwrap.fill(message.body if message.body else '', replace_whitespace=False, drop_whitespace=False), '| ', predicate=lambda line: True)}
+{'-' * 80}+
"""

    def _format_choice(self, choice: MultipleChoice) -> str:
        message = choice.message
        retval = f"""+{'-' * 80}+
|
| {message.sender} -> {message.recepient}: {message.heading if message.heading else ''}
|
{textwrap.indent(textwrap.fill(message.body if message.body else '', replace_whitespace=False, drop_whitespace=False), '| ', predicate=lambda line: True)}
|
"""
        if choice.single:
            retval += f"Please select one of the following options: {', '.join(choice.choices)}"
        else:
            retval += f"Please select one or more of the following options: {', '.join(choice.choices)}"

        if choice.default:
            retval += f" (default: {choice.default})" + "\n"
        else:
            retval += "\n"

        retval += f"+{'-' * 100}"

        return retval

    def _indent(self, text: str) -> str:
        return textwrap.indent(text, " " * 4 * self.level)

    def input(self, message: ChatMessage, *, password: bool = False) -> str:
        prompt = self._format_message(message)
        prompt = self._indent(prompt)
        if password:
            return getpass.getpass(prompt)
        else:
            return input(prompt)

    def print(self, message: ChatMessage) -> None:
        msg = self._format_message(message)
        msg = self._indent(msg)

        print(msg)  # noqa: T201 `print` found

    def select(self, choice: MultipleChoice) -> str:
        # message = choice.message
        prompt = self._format_choice(choice)

        while True:
            prompt = self._indent(prompt)
            value = input(prompt)
            if value == "" and choice.default:
                return choice.default

            if choice.single:
                if value in choice.choices:
                    return value
                else:
                    prompt = "Invalid choice. Please try again.\n\n"

            else:
                values = [x.strip() for x in value.split(",")]

                bad_choices = [v for v in values if v not in choice.choices]
                if any(bad_choices):
                    prompt = (
                        f"Invalid choices ({', '.join(bad_choices)})."
                        + " Please try again.\n\n"
                    )
                else:
                    return value

    def create_subconversation(self) -> "ConsoleIO":
        sub_conversation = ConsoleIO(self)
        self.sub_conversations.append(sub_conversation)

        return sub_conversation
