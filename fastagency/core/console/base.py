import getpass
import json
import textwrap
from dataclasses import asdict, dataclass
from typing import List, Optional

from fastagency.core.base import IOStreamingMessage

from ..base import IOMessage, MultipleChoiceContent, TextInputContent


class ConsoleIO:  # Chatable
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
        self.sub_conversations: List[ConsoleIO] = []

    @property
    def level(self) -> int:
        return (
            0 if self.super_conversation is None else self.super_conversation.level + 1
        )

    def _format_message(self, message: ConsoleMessage) -> str:
        return f"""+{'-' * 80}+
|
| {message.sender} -> {message.recepient}: {message.heading if message.heading else ''}
|
{textwrap.indent(textwrap.fill(message.body if message.body else '', replace_whitespace=False, drop_whitespace=False), '| ', predicate=lambda line: True)}
+{'-' * 80}+
"""

    #     def _format_choice(self, choice: MultipleChoice) -> str:
    #         message = choice.message
    #         retval = f"""+{'-' * 80}+
    # |
    # | {message.sender} -> {message.recepient}: {message.heading if message.heading else ''}
    # |
    # {textwrap.indent(textwrap.fill(message.body if message.body else '', replace_whitespace=False, drop_whitespace=False), '| ', predicate=lambda line: True)}
    # |
    # """
    #         if choice.single:
    #             retval += f"Please select one of the following options: {', '.join(choice.choices)}"
    #         else:
    #             retval += f"Please select one or more of the following options: {', '.join(choice.choices)}"

    #         if choice.default:
    #             retval += f" (default: {choice.default})" + "\n"
    #         else:
    #             retval += "\n"

    #         retval += f"+{'-' * 100}"

    #         return retval

    def _indent(self, text: str) -> str:
        return textwrap.indent(text, " " * 4 * self.level)

    def process_text_message(self, message: IOMessage) -> None:
        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recepient=message.recepient,
            heading=message.heading,
            body=message.content.body,
        )
        msg = self._format_message(console_msg)
        msg = self._indent(msg)

        print(msg)  # noqa: T201 `print` found

    def process_text_input(self, message: IOMessage) -> str:
        content: TextInputContent = message.content

        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recepient=message.recepient,
            heading=message.heading,
            body=f"{content.prompt} (suggestions: {', '.join(content.suggestions)})",
        )
        password = message.content.password

        prompt = self._format_message(console_msg)
        prompt = self._indent(prompt)
        if password:
            return getpass.getpass(prompt)
        else:
            return input(prompt)

    def process_multiple_choice(self, message: IOMessage) -> str:
        content: MultipleChoiceContent = message.content

        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recepient=message.recepient,
            heading=message.heading,
            body=f"{content.prompt} (choices: {', '.join(content.choices)}, default: {content.default})",
        )

        prompt = self._format_message(console_msg)
        prompt = self._indent(prompt)
        while True:
            retval = input(prompt)
            if retval in content.choices:
                return retval
            else:
                print(f"Invalid choice ('{retval}'). Please try again.")  # noqa: T201 `print` found

    def process_other(self, message: IOMessage) -> None:
        console_msg = self.ConsoleMessage(
            sender=message.sender,
            recepient=message.recepient,
            heading=f"Message type: {message.type}",
            body=json.dumps(asdict(message.content), indent=2),
        )
        msg = self._format_message(console_msg)
        msg = self._indent(msg)

        print(msg)  # noqa: T201 `print` found

    def process_message(self, message: IOMessage) -> str | None:
        if message.type == "text_message":
            return self.process_text_message(message)
        elif message.type == "text_input":
            return self.process_text_input(message)
        elif message.type == "multiple_choice":
            return self.process_multiple_choice(message)
        else:
            return self.process_other(message)

    def process_streaming_message(self, message: IOStreamingMessage) -> str | None:
        raise NotImplementedError

    def create_subconversation(self) -> "ConsoleIO":
        sub_conversation = ConsoleIO(self)
        self.sub_conversations.append(sub_conversation)

        return sub_conversation


# class ConsoleIO(Chatable):
#     def __init__(self, super_conversation: Optional["ConsoleIO"] = None) -> None:
#         """Initialize the console IO object.

#         Args:
#             super_conversation (Optional[Chatable], optional): The super conversation. Defaults to None.
#         """
#         self.super_conversation: Optional[ConsoleIO] = super_conversation
#         self.sub_conversations: List[ConsoleIO] = []

#     @property
#     def level(self) -> int:
#         return (
#             0 if self.super_conversation is None else self.super_conversation.level + 1
#         )

#     def _format_message(self, message: IOMessage) -> str:
#         return f"""+{'-' * 80}+
# |
# | {message.sender} -> {message.recepient}: {message.heading if message.heading else ''}
# |
# {textwrap.indent(textwrap.fill(message.body if message.body else '', replace_whitespace=False, drop_whitespace=False), '| ', predicate=lambda line: True)}
# +{'-' * 80}+
# """

#     def _format_choice(self, choice: MultipleChoice) -> str:
#         message = choice.message
#         retval = f"""+{'-' * 80}+
# |
# | {message.sender} -> {message.recepient}: {message.heading if message.heading else ''}
# |
# {textwrap.indent(textwrap.fill(message.body if message.body else '', replace_whitespace=False, drop_whitespace=False), '| ', predicate=lambda line: True)}
# |
# """
#         if choice.single:
#             retval += f"Please select one of the following options: {', '.join(choice.choices)}"
#         else:
#             retval += f"Please select one or more of the following options: {', '.join(choice.choices)}"

#         if choice.default:
#             retval += f" (default: {choice.default})" + "\n"
#         else:
#             retval += "\n"

#         retval += f"+{'-' * 100}"

#         return retval

#     def _indent(self, text: str) -> str:
#         return textwrap.indent(text, " " * 4 * self.level)

#     def input(self, message: IOMessage, *, password: bool = False) -> str:
#         prompt = self._format_message(message)
#         prompt = self._indent(prompt)
#         if password:
#             return getpass.getpass(prompt)
#         else:
#             return input(prompt)

#     def print(self, message: IOMessage) -> None:
#         msg = self._format_message(message)
#         msg = self._indent(msg)

#         print(msg)  # `print` found

#     def select(self, choice: MultipleChoice) -> str:
#         # message = choice.message
#         prompt = self._format_choice(choice)

#         while True:
#             prompt = self._indent(prompt)
#             value = input(prompt)
#             if value == "" and choice.default:
#                 return choice.default

#             if choice.single:
#                 if value in choice.choices:
#                     return value
#                 else:
#                     prompt = "Invalid choice. Please try again.\n\n"

#             else:
#                 values = [x.strip() for x in value.split(",")]

#                 bad_choices = [v for v in values if v not in choice.choices]
#                 if any(bad_choices):
#                     prompt = (
#                         f"Invalid choices ({', '.join(bad_choices)})."
#                         + " Please try again.\n\n"
#                     )
#                 else:
#                     return value

#     def create_subconversation(self) -> "ConsoleIO":
#         sub_conversation = ConsoleIO(self)
#         self.sub_conversations.append(sub_conversation)

#         return sub_conversation
