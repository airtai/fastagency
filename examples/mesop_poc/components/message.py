import json
import mesop as me
from typing import Optional

from fastagency.core.base import IOMessage
from fastagency.core.mesop.base import IOMessageVisitor, TextInput, TextMessage, MultipleChoice

def message_box(message: str):
    message_dict = json.loads(message)
    level = message_dict["level"]
    conversationId = message_dict["conversationId"]
    io_message_dict = message_dict["io_message"]
    io_message = IOMessage.create(**io_message_dict)
    visitor = MesopGUIMessageVisitor(level, conversationId)
    visitor.process_message(io_message)

class MesopGUIMessageVisitor(IOMessageVisitor):
    def __init__(self, level, conversationId):
        self._level = level
        self._conversationId = conversationId

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
        text = message.prompt + "\n" + ",".join([f"{suggestion}" for i, suggestion in enumerate(message.suggestions)])
        with me.box(
            style=me.Style(
                background="#bff",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            me.markdown(text)

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        text = message.prompt + "\n" + "\n".join([f"{i+1}. {choice}" for i, choice in enumerate(message.choices)])
        with me.box(
            style=me.Style(
                background="#cff",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            me.markdown(text)

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)
