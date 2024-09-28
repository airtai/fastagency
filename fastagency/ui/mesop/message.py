import json
from collections.abc import Iterable, Iterator
from typing import Optional
from uuid import uuid4

import mesop as me

from fastagency.base import AskingMessage, WorkflowCompleted
from fastagency.ui.mesop.base import MesopMessage
from fastagency.ui.mesop.components.inputs import input_text
from fastagency.ui.mesop.send_prompt import send_user_feedback_to_autogen

from ...base import (
    FunctionCallExecution,
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    SuggestedFunctionCall,
    SystemMessage,
    TextInput,
    TextMessage,
)
from .components.helpers import darken_hex_color
from .data_model import Conversation, ConversationMessage, State


def consume_responses(responses: Iterable[MesopMessage]) -> Iterator[None]:
    for message in responses:
        state = me.state(State)
        handle_message(state, message)
        yield
        me.scroll_into_view(key="end_of_messages")
        yield
    yield


def message_box(message: ConversationMessage, read_only: bool) -> None:
    io_message_dict = json.loads(message.io_message_json)
    level = message.level
    conversation_id = message.conversation_id
    io_message = IOMessage.create(**io_message_dict)
    visitor = MesopGUIMessageVisitor(level, conversation_id, message, read_only)
    visitor.process_message(io_message)


def handle_message(state: State, message: MesopMessage) -> None:
    conversation = state.conversation
    messages = conversation.messages
    level = message.conversation.level
    conversation_id = message.conversation.id
    io_message = message.io_message
    message_dict = io_message.model_dump()
    message_json = json.dumps(message_dict)
    conversation_message = ConversationMessage(
        level=level,
        conversation_id=conversation_id,
        io_message_json=message_json,
        feedback=[],
    )
    messages.append(conversation_message)
    conversation.messages = list(messages)
    if isinstance(io_message, AskingMessage):
        conversation.waiting_for_feedback = True
        conversation.completed = False
    if isinstance(io_message, WorkflowCompleted):
        conversation.completed = True
        conversation.waiting_for_feedback = False
        if not conversation.is_from_the_past:
            uuid: str = uuid4().hex
            becomme_past = Conversation(
                id=uuid,
                title=conversation.title,
                messages=conversation.messages,
                completed=True,
                is_from_the_past=True,
                waiting_for_feedback=False,
            )
            state.past_conversations.insert(0, becomme_past)


class MesopGUIMessageVisitor(IOMessageVisitor):
    def __init__(
        self,
        level: int,
        conversation_id: str,
        conversation_message: ConversationMessage,
        read_only: bool = False,
    ) -> None:
        """Initialize the MesopGUIMessageVisitor object.

        Args:
            level (int): The level of the message.
            conversation_id (str): The ID of the conversation.
            conversation_message (ConversationMessage): Conversation message that wraps the visited io_message
            read_only (bool): Input messages are disabled in read only mode
        """
        self._level = level
        self._conversation_id = conversation_id
        self._readonly = read_only
        self._conversation_message = conversation_message

    def _has_feedback(self) -> bool:
        return len(self._conversation_message.feedback) > 0

    def _is_completed(self) -> bool:
        return self._conversation_message.feedback_completed

    def _provide_feedback(self, feedback: str) -> Iterator[None]:
        state = me.state(State)
        conversation = state.conversation
        conversation.feedback = ""
        conversation.waiting_for_feedback = False
        yield
        me.scroll_into_view(key="end_of_messages")
        yield
        responses = send_user_feedback_to_autogen(feedback)
        yield from consume_responses(responses)

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
                align_self="flex-start",
                width="95%",
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Text message")
            me.markdown(message.body)

    def visit_system_message(self, message: SystemMessage) -> None:
        base_color = "#bff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="System Message")
            me.markdown(json.dumps(message.message, indent=2))

    def visit_text_input(self, message: TextInput) -> str:
        def on_input(feedback: str) -> Iterator[None]:
            self._conversation_message.feedback = [feedback]
            self._conversation_message.feedback_completed = True
            yield from self._provide_feedback(feedback)

        def value_if_completed() -> Optional[str]:
            message = self._conversation_message
            return message.feedback[0] if message.feedback_completed else None

        base_color = "#dff"
        prompt = message.prompt if message.prompt else "Please enter a value"
        if message.suggestions:
            suggestions = ",".join(suggestion for suggestion in message.suggestions)
            prompt += "\n Suggestions: " + suggestions

        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                align_self="flex-end",
                width="95%",
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Input requested")
            me.markdown(prompt)
            input_text(
                on_input,
                "prompt",
                disabled=self._readonly or self._has_feedback(),
                value=value_if_completed(),
            )
        return ""

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        if message.single:
            return self._visit_single_choice(message)
        else:
            return self._visit_many_choices(message)

    def _visit_single_choice(self, message: MultipleChoice) -> str:
        def on_change(ev: me.RadioChangeEvent) -> Iterator[None]:
            feedback = ev.value
            self._conversation_message.feedback = [feedback]
            self._conversation_message.feedback_completed = True
            yield from self._provide_feedback(feedback)

        base_color = "#dff"
        prompt = message.prompt if message.prompt else "Please enter a value"
        if message.choices:
            options = (
                me.RadioOption(
                    label=(choice if choice != message.default else choice + " *"),
                    value=choice,
                )
                for choice in message.choices
            )
        if self._has_feedback():
            pre_selected = {"value": self._conversation_message.feedback[0]}
        else:
            pre_selected = {}
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                border_radius=16,
                align_self="flex-end",
                width="95%",
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Input requested")
            me.text(prompt)
            me.radio(
                on_change=on_change,
                disabled=self._readonly or self._is_completed(),
                options=options,
                style=me.Style(display="flex", flex_direction="column"),
                **pre_selected,
            )
        return ""

    def _visit_many_choices(self, message: MultipleChoice) -> str:
        def on_change(ev: me.CheckboxChangeEvent) -> None:
            message_feedback = self._conversation_message.feedback
            choice = ev.key
            yes_no = ev.checked
            if yes_no:
                if choice not in message_feedback:
                    message_feedback.append(choice)
            else:
                if choice in message_feedback:
                    message_feedback.remove(choice)

        def on_click(ev: me.ClickEvent) -> Iterator[None]:
            message_feedback = self._conversation_message.feedback
            feedback = ",".join(message_feedback)
            self._conversation_message.feedback_completed = True
            yield from self._provide_feedback(feedback)

        def should_be_checked(option: str) -> bool:
            conversation_message = self._conversation_message
            return option in conversation_message.feedback

        base_color = "#dff"
        prompt = message.prompt if message.prompt else "Please enter a value"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                align_self="flex-end",
                width="95%",
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Input requested")
            me.text(prompt)
            if message.choices:
                with me.box(style=me.Style(display="flex", flex_direction="column")):
                    for option in message.choices:
                        me.checkbox(
                            label=option,
                            key=option,
                            checked=should_be_checked(option),
                            on_change=on_change,
                            disabled=self._readonly or self._is_completed(),
                        )
            me.button(label="Ok", on_click=on_click)
        return ""

    def visit_suggested_function_call(
        self, message: SuggestedFunctionCall
    ) -> Optional[str]:
        base_color = "#8ff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                align_self="flex-start",
                width="95%",
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Suggested Function Call")
            with me.box():
                me.text(message.function_name)
            me.markdown(json.dumps(message.arguments))
        return ""

    def visit_function_call_execution(
        self, message: FunctionCallExecution
    ) -> Optional[str]:
        base_color = "#7ff"
        with me.box(
            style=me.Style(
                background=base_color,
                padding=me.Padding.all(16),
                align_self="flex-start",
                width="95%",
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            self._header(message, base_color, title="Function Call Execution")
            with me.box():
                me.text(message.function_name)
            me.markdown(json.dumps(message.retval))
        return ""

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)

    def _header(
        self, message: IOMessage, base_color: str, title: Optional[str] = None
    ) -> None:
        you_want_it_darker = darken_hex_color(base_color, 0.8)
        with me.box(
            style=me.Style(
                background=you_want_it_darker,
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin.symmetric(vertical=16),
            )
        ):
            h = title if title else message.type
            if message.sender and message.recipient:
                h += f": {message.sender} -> {message.recipient}"
            elif message.sender:
                h += f": to {message.sender}"
            elif message.recipient:
                h += f": from {message.recipient}"
            if message.auto_reply:
                h += " (auto-reply)"
            me.markdown(h)
