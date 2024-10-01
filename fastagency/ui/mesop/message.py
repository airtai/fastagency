import json
from collections.abc import Iterable, Iterator
from typing import Any, Callable, Optional
from uuid import uuid4

import mesop as me

from ...base import (
    AskingMessage,
    FunctionCallExecution,
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    SuggestedFunctionCall,
    SystemMessage,
    TextInput,
    TextMessage,
    WorkflowCompleted,
)
from ...logging import get_logger
from .base import MesopMessage
from .components.inputs import input_text
from .data_model import Conversation, ConversationMessage, State
from .send_prompt import send_user_feedback_to_autogen
from .styles import MesopHomePageStyles, MesopMessageStyles

logger = get_logger(__name__)


def dict_to_markdown(d: dict[str, Any], *, indent: int = 2) -> str:
    return "\n```\n" + json.dumps(d, indent=2) + "\n```\n"


def consume_responses(responses: Iterable[MesopMessage]) -> Iterator[None]:
    for message in responses:
        state = me.state(State)
        handle_message(state, message)
        yield
        me.scroll_into_view(key="end_of_messages")
        yield
    yield


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


def message_box(
    message: ConversationMessage, read_only: bool, *, styles: MesopHomePageStyles
) -> None:
    io_message_dict = json.loads(message.io_message_json)
    level = message.level
    conversation_id = message.conversation_id
    io_message = IOMessage.create(**io_message_dict)
    visitor = MesopGUIMessageVisitor(level, conversation_id, message, styles, read_only)
    visitor.process_message(io_message)


class MesopGUIMessageVisitor(IOMessageVisitor):
    def __init__(
        self,
        level: int,
        conversation_id: str,
        conversation_message: ConversationMessage,
        styles: MesopHomePageStyles,
        read_only: bool = False,
    ) -> None:
        """Initialize the MesopGUIMessageVisitor object.

        Args:
            level (int): The level of the message.
            conversation_id (str): The ID of the conversation.
            conversation_message (ConversationMessage): Conversation message that wraps the visited io_message
            styles (MesopHomePageStyles): Styles for the message
            read_only (bool): Input messages are disabled in read only mode
        """
        self._level = level
        self._conversation_id = conversation_id
        self._readonly = read_only
        self._conversation_message = conversation_message
        self._styles = styles

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

    def message_content_to_markdown(self, msg: IOMessage) -> str:
        d = msg.model_dump()
        d.pop("sender")
        d.pop("recipient")
        d.pop("type")

        return "\n".join([f"**{k}**: {v} <br>" for k, v in d["content"].items()])

    def visit_default(
        self,
        message: IOMessage,
        *,
        content: Optional[str] = None,
        style: Optional[MesopMessageStyles] = None,
        error: Optional[bool] = False,
        inner_callback: Optional[Callable[..., None]] = None,
    ) -> None:
        logger.info(f"visit_default: {message=}")
        style = style or self._styles.message.default
        title = message.type.replace("_", " ").capitalize()
        title = "[Error] " + title if error else title
        with me.box(style=style.box or self._styles.message.default.box):
            self._header(
                message,
                title=title,
                box_style=style.header_box,
                md_style=style.header_md,
            )

            content = content or self.message_content_to_markdown(message)

            me.markdown(content, style=style.md or self._styles.message.default.md)

            if inner_callback:
                inner_callback()

    def visit_text_message(self, message: TextMessage) -> None:
        content = message.body if message.body else ""
        content = content if content.strip() != "" else "*(empty message)*"
        self.visit_default(
            message,
            content=content,
            style=self._styles.message.text,
        )

    def visit_system_message(self, message: SystemMessage) -> None:
        content = (
            f"""#### **{message.message['heading']}**

{message.message['body']}
"""
            if "heading" in message.message and "body" in message.message
            else None
        )

        self.visit_default(
            message,
            content=content,
            style=self._styles.message.system,
        )

    def visit_suggested_function_call(self, message: SuggestedFunctionCall) -> None:
        content = f"""
**function_name**: `{message.function_name}`<br>
**call_id**: `{message.call_id}`<br>
**arguments**:
{dict_to_markdown(message.arguments)}
"""
        self.visit_default(
            message,
            content=content,
            style=self._styles.message.suggested_function_call,
        )

    def visit_function_call_execution(self, message: FunctionCallExecution) -> None:
        return self.visit_default(
            message,
            style=self._styles.message.function_call_execution,
        )

    def visit_text_input(self, message: TextInput) -> str:
        def on_input(feedback: str) -> Iterator[None]:
            self._conversation_message.feedback = [feedback]
            self._conversation_message.feedback_completed = True
            yield from self._provide_feedback(feedback)

        def value_if_completed() -> Optional[str]:
            message = self._conversation_message
            return message.feedback[0] if message.feedback_completed else None

        # base_color = "#dff"
        prompt = message.prompt if message.prompt else "Please enter a value"
        if message.suggestions:
            suggestions = ",".join(suggestion for suggestion in message.suggestions)
            prompt += "\n Suggestions: " + suggestions

        self.visit_default(
            message,
            content=prompt,
            style=self._styles.message.text_input,
            inner_callback=lambda: input_text(
                on_input,
                key="prompt",
                disabled=self._readonly or self._has_feedback(),
                value=value_if_completed(),
                style=self._styles.message.text_input_inner,
            ),
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

        # base_color = "#dff"
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

        def inner_callback() -> None:
            me.radio(
                on_change=on_change,
                disabled=self._readonly or self._is_completed(),
                options=options,
                style=self._styles.message.single_choice_inner.radio,
                **pre_selected,
            )

        self.visit_default(
            message,
            content=prompt,
            style=self._styles.message.text_input,
            inner_callback=inner_callback,
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

        prompt = message.prompt if message.prompt else "Please select a value:"

        def inner_callback() -> None:
            if message.choices:
                with me.box(
                    style=self._styles.message.multiple_choice_inner.box,
                ):
                    for option in message.choices:
                        me.checkbox(
                            label=option,
                            key=option,
                            checked=should_be_checked(option),
                            on_change=on_change,
                            disabled=self._readonly or self._is_completed(),
                            style=self._styles.message.multiple_choice_inner.checkbox,
                        )
                    me.button(
                        label="OK",
                        on_click=on_click,
                        color="primary",
                        type="flat",
                        style=self._styles.message.multiple_choice_inner.button,
                    )

        self.visit_default(
            message,
            content=prompt,
            style=self._styles.message.text_input,
            inner_callback=inner_callback,
        )
        return ""

    def render_error_message(
        self,
        e: Exception,
        message: IOMessage,
        *,
        content: Optional[str] = None,
        style: Optional[MesopMessageStyles] = None,
    ) -> None:
        style = self._styles.message.error or self._styles.message.default
        title = "[Error] " + message.type.replace("_", " ").capitalize()

        with me.box(style=style.box or self._styles.message.default.box):
            self._header(
                message,
                title=title,
                box_style=style.header_box or self._styles.message.default.header_box,
                md_style=style.header_md or self._styles.message.default.header_md,
            )

            content = (
                "Failed to render message:"
                + dict_to_markdown(message.model_dump())
                + f"<br>Error: {e}"
            )

            logger.info(f"render_error_message: {content=}")
            me.markdown(content, style=style.md or self._styles.message.default.md)

    def process_message(self, message: IOMessage) -> Optional[str]:
        try:
            return self.visit(message)
        except Exception as e:
            logger.warning(f"Failed to render message: {e}")
            self.render_error_message(e, message)
            return None

    def _header(
        self,
        message: IOMessage,
        *,
        title: Optional[str] = None,
        box_style: Optional[me.Style] = None,
        md_style: Optional[me.Style] = None,
    ) -> None:
        with me.box(style=box_style or self._styles.message.default.header_box):
            h = title if title else message.type
            if message.sender and message.recipient:
                h += f": {message.sender} -> {message.recipient}"
            elif message.sender:
                h += f": to {message.sender}"
            elif message.recipient:
                h += f": from {message.recipient}"
            if message.auto_reply:
                h += " (auto-reply)"
            h = f"**{h}**"
            # style=me.Style(padding=me.Padding(top=8, right=16, left=16, bottom=8))
            me.markdown(h, style=md_style or self._styles.message.default.header_md)
