import json
from typing import Optional

import mesop as me

from fastagency.core.base import (
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    TextInput,
    TextMessage,
)


def message_box(message: str) -> None:
    message_dict = json.loads(message)
    level = message_dict["level"]
    conversation_id = message_dict["conversationId"]
    io_message_dict = message_dict["io_message"]
    io_message = IOMessage.create(**io_message_dict)
    visitor = MesopGUIMessageVisitor(level, conversation_id)
    visitor.process_message(io_message)


class MesopGUIMessageVisitor(IOMessageVisitor):
    def __init__(self, level: int, conversation_id: str) -> None:
        """Initialize the MesopGUIMessageVisitor object.

        Args:
            level (int): The level of the message.
            conversation_id (str): The ID of the conversation.
        """
        self._level = level
        self._conversation_id = conversation_id

    def visit_default(self, message: IOMessage) -> None:
        with me.box(
            style=me.Style(
                background="#aff",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            me.markdown(message.type)

    def visit_text_message(self, message: TextMessage) -> None:
        with me.box(
            style=me.Style(
                background="#fff",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            me.markdown(message.body)

    def visit_text_input(self, message: TextInput) -> str:
        text = message.prompt if message.prompt else "Please enter a value"
        if message.suggestions:
            suggestions = ",".join(suggestion for suggestion in message.suggestions)
            text += "\n" + suggestions

        with me.box(
            style=me.Style(
                background="#bff",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            me.markdown(text)
        return ""

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        text = message.prompt if message.prompt else "Please enter a value"
        if message.choices:
            options = ",".join(
                f"{i+1}. {choice}" for i, choice in enumerate(message.choices)
            )
            text += "\n" + options
        with me.box(
            style=me.Style(
                background="#cff",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            me.markdown(text)
        return ""

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)
