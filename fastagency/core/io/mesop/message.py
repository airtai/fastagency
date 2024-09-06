import json
from typing import Optional

import mesop as me

from ...base import (
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
        base_color = "#aff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color)
            me.markdown(message.type)

    def visit_text_message(self, message: TextMessage) -> None:
        base_color = "#fff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color)
            me.markdown(message.body)

    def visit_text_input(self, message: TextInput) -> str:
        text = message.prompt if message.prompt else "Please enter a value"
        if message.suggestions:
            suggestions = ",".join(suggestion for suggestion in message.suggestions)
            text += "\n" + suggestions

        base_color = "#bff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color)
            me.markdown(text)
        return ""

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        text = message.prompt if message.prompt else "Please enter a value"
        if message.choices:
            options = ",".join(
                f"{i+1}. {choice}" for i, choice in enumerate(message.choices)
            )
            text += "\n" + options
        base_color = "#cff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color)
            me.markdown(text)
        return ""

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)

    def _header(self, message: IOMessage, base_color: str) -> None:
        you_want_it_darker = darken_hex_color(base_color, 0.8)
        with me.box(
            style=me.Style(
                background=you_want_it_darker,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            h = f"From: {message.sender}, to:{message.recepient}"
            if message.auto_reply:
                h += " (auto-reply)"
            me.markdown(h)


def darken_hex_color(hex_color: str, factor: float = 0.8) -> str:
    """Darkens a hex color by a given factor.

    Args:
    hex_color: The hex color code (e.g., '#FF0000').
    factor: The darkening factor (0.0 to 1.0, where 1.0 is no change and 0.0 is completely dark).

    Returns:
    The darkened hex color code.
    """
    # Remove the '#' prefix if it exists
    hex_color = hex_color.lstrip("#")

    if len(hex_color) == 3:
        hex_color = "".join(char * 2 for char in hex_color)

    # Convert hex to RGB values
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    # Darken each component
    darkened_rgb = tuple(int(channel * factor) for channel in rgb)

    # Convert back to hex
    darkened_hex = "#{:02X}{:02X}{:02X}".format(*darkened_rgb)

    return darkened_hex
