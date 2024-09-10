import json
import os
from collections.abc import Iterator

import mesop as me

from fastagency.cli.discover import import_from_string
from fastagency.core.base import AskingMessage, WorkflowCompleted, Workflows
from fastagency.core.io.mesop.base import MesopMessage
from fastagency.core.io.mesop.components.inputs import input_prompt, input_user_feedback
from fastagency.core.io.mesop.components.ui_common import conversation_completed, header
from fastagency.core.io.mesop.data_model import Conversation, State
from fastagency.core.io.mesop.message import message_box
from fastagency.core.io.mesop.send_prompt import (
    send_prompt_to_autogen,
    send_user_feedback_to_autogen,
)
from fastagency.logging import get_logger
from fastagency.core.io.mesop.styles import (
    CHAT_STARTER_STYLE,
    PAST_CHATS_STYLE,
    ROOT_BOX_STYLE,
    STYLESHEETS,
)

# Get the logger
logger = get_logger(__name__)


def get_workflows() -> Workflows:
    import_string = os.environ.get("IMPORT_STRING", None)
    if import_string is None:
        raise ValueError("No import string provided")

    # import app using import string
    app = import_from_string(import_string)

    # get workflows from the app
    wf = app.wf

    return wf


SECURITY_POLICY = me.SecurityPolicy(allowed_iframe_parents=["https://huggingface.co"])


@me.page(  # type: ignore[misc]
    path="/",
    stylesheets=STYLESHEETS,
    security_policy=SECURITY_POLICY,
)
def home_page() -> None:
    state = me.state(State)
    with me.box(style=ROOT_BOX_STYLE):
        past_conversations_box()
        if state.in_conversation:
            conversation_box()
        else:
            conversation_starter_box()


def past_conversations_box() -> None:
    def _select_past_conversation(ev: me.ClickEvent) -> None:
        me.navigate("/past", query_params={"id": ev.key})

    state = me.state(State)
    with me.box(style=PAST_CHATS_STYLE):
        for conversation in state.past_conversations:
            with me.box(
                key=conversation.id,  # they are GUIDs so should not clash with anything other on the page
                on_click=_select_past_conversation,
                style=me.Style(
                    width="min(200px)",
                    margin=me.Margin.symmetric(horizontal="auto", vertical=36),
                ),
            ):
                me.text(
                    text=conversation.title,
                )


def conversation_starter_box() -> None:
    with me.box(style=CHAT_STARTER_STYLE):
        header()
        with me.box(
            style=me.Style(
                width="min(680px, 100%)",
                margin=me.Margin.symmetric(horizontal="auto", vertical=36),
            )
        ):
            me.text(
                "Enter a prompt to chat with Autogen team",
                style=me.Style(font_size=20, margin=me.Margin(bottom=24)),
            )
            input_prompt(send_prompt)


def _handle_message(state: State, message: MesopMessage) -> None:
    conversation = state.conversation
    messages = conversation.messages
    level = message.conversation.level
    conversation_id = message.conversation.id
    io_message = message.io_message
    message_dict = io_message.model_dump()
    message_string = json.dumps(
        {"level": level, "conversationId": conversation_id, "io_message": message_dict}
    )
    messages.append(message_string)
    conversation.messages = list(messages)
    if isinstance(io_message, AskingMessage):
        conversation.waiting_for_feedback = True
        conversation.completed = False
    if isinstance(io_message, WorkflowCompleted):
        conversation.completed = True
        conversation.waiting_for_feedback = False


def send_prompt(e: me.ClickEvent) -> Iterator[None]:
    wf = get_workflows()
    name = wf.names[0]

    state = me.state(State)
    # me.navigate("/conversation")
    prompt = state.prompt
    state.prompt = ""
    conversation = Conversation(
        title=prompt, completed=False, waiting_for_feedback=False
    )
    state.conversation = conversation
    state.in_conversation = True
    yield
    responses = send_prompt_to_autogen(prompt=prompt, wf=wf, name=name)
    for message in responses:
        state = me.state(State)
        _handle_message(state, message)
        yield
        me.scroll_into_view(key="end_of_messages")
        yield
    yield


def conversation_box() -> None:
    state = me.state(State)
    conversation = state.conversation
    with me.box(style=ROOT_BOX_STYLE):
        header()
        messages = conversation.messages
        with me.box(
            style=me.Style(
                overflow_y="auto",
            )
        ):
            for message in messages:
                message_box(message)
            if messages:
                me.box(
                    key="end_of_messages",
                    style=me.Style(margin=me.Margin(bottom="50vh")),
                )
        if conversation.waiting_for_feedback:
            input_user_feedback(on_user_feedback)
        if conversation.completed:
            conversation_completed(reset_conversation)


@me.page(path="/conversation", stylesheets=STYLESHEETS, security_policy=SECURITY_POLICY)  # type: ignore[misc]
def conversation_page() -> None:
    state = me.state(State)
    with me.box(style=ROOT_BOX_STYLE):
        header()
        messages = state.conversation.messages
        with me.box(
            style=me.Style(
                overflow_y="auto",
            )
        ):
            for message in messages:
                message_box(message)
            if messages:
                me.box(
                    key="end_of_messages",
                    style=me.Style(margin=me.Margin(bottom="50vh")),
                )
        if state.waiting_for_feedback:
            input_user_feedback(on_user_feedback)
        if state.conversation_completed:
            conversation_completed(reset_conversation)


@me.page(path="/past", stylesheets=STYLESHEETS, security_policy=SECURITY_POLICY)  # type: ignore[misc]
def past_conversation_page() -> None:
    id = me.query_params.get("id")
    state = me.state(State)
    conversations_with_id = list(filter(lambda c: c.id == id, state.past_conversations))
    conversation = conversations_with_id[0]

    with me.box(style=ROOT_BOX_STYLE):
        header()
        messages = conversation.messages
        with me.box(
            style=me.Style(
                overflow_y="auto",
            )
        ):
            for message in messages:
                message_box(message)
            if messages:
                me.box(
                    key="end_of_messages",
                    style=me.Style(margin=me.Margin(bottom="50vh")),
                )
        with me.box(on_click=me.navigate("/")):
            me.text(text="back")


def reset_conversation() -> None:
    state = me.state(State)
    state.in_conversation = False
    # state.conversation_completed = False
    # state.conversation.messages = []
    # state.waiting_for_feedback = False
    state.prompt = ""


def on_user_feedback(e: me.ClickEvent) -> Iterator[None]:
    state = me.state(State)
    conversation = state.conversation
    feedback = conversation.feedback
    conversation.feedback = ""
    conversation.waiting_for_feedback = False
    yield
    me.scroll_into_view(key="end_of_messages")
    yield
    responses = send_user_feedback_to_autogen(feedback)
    for message in responses:
        state = me.state(State)
        _handle_message(state, message)
        yield
        me.scroll_into_view(key="end_of_messages")
        yield
    yield
