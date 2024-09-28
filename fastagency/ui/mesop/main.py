import time
from collections.abc import Iterator
from typing import TYPE_CHECKING, Callable, Optional

import mesop as me

from ...logging import get_logger
from .components.inputs import input_text
from .components.ui_common import header
from .data_model import Conversation, State
from .message import consume_responses, message_box
from .send_prompt import send_prompt_to_autogen
from .styles import (
    CHAT_STARTER_STYLE,
    PAST_CHATS_HIDE_STYLE,
    PAST_CHATS_SHOW_STYLE,
    ROOT_BOX_STYLE,
    STYLESHEETS,
)

if TYPE_CHECKING:
    from .base import MesopUI

__all__ = ["me"]

# Get the logger
logger = get_logger(__name__)

_ui: Optional["MesopUI"] = None


def get_ui() -> "MesopUI":
    global _ui

    if _ui is None:
        logger.error("get_ui(): MesopUI instance is None")
        raise ValueError("MesopUI instance is None")

    return _ui


SECURITY_POLICY = me.SecurityPolicy(allowed_iframe_parents=["https://huggingface.co"])


def create_home_page(ui: "MesopUI") -> Callable[[], None]:
    global _ui
    _ui = ui

    @me.page(  # type: ignore[misc]
        path="/",
        stylesheets=STYLESHEETS,
        security_policy=SECURITY_POLICY,
    )
    def home_page() -> None:
        # check if we have access to the MesopUI instance
        ui = get_ui()
        if ui is None:
            logger.error("home_page(): MesopUI instance is None")
            me.text(text="Error: MesopUI instance is None. Something went wrong.")
            return

        try:
            state = me.state(State)
            with me.box(style=ROOT_BOX_STYLE):
                past_conversations_box()
                if state.in_conversation:
                    conversation_box()
                else:
                    conversation_starter_box()
        except Exception as e:
            logger.error(f"home_page(): Error rendering home page: {e}")
            me.text(text="Error: Something went wrong, please check logs for details.")

        return

    return home_page  # type: ignore[no-any-return]


def past_conversations_box() -> None:
    def conversation_display_title(full_name: str, max_length: int) -> str:
        if len(full_name) <= max_length:
            return full_name
        else:
            return full_name[: max_length - 3] + "..."

    def select_past_conversation(ev: me.ClickEvent) -> Iterator[None]:
        id = ev.key
        state = me.state(State)
        conversations_with_id = list(
            filter(lambda c: c.id == id, state.past_conversations)
        )
        conversation = conversations_with_id[0]
        state.conversation = conversation
        state.in_conversation = True
        yield
        time.sleep(1)
        yield
        me.scroll_into_view(key="conversationtop")
        yield

    def on_show_hide(ev: me.ClickEvent) -> None:
        state.hide_past = not state.hide_past

    def on_start_new_conversation(ev: me.ClickEvent) -> None:
        state.in_conversation = False
        state.prompt = ""

    state = me.state(State)
    style = PAST_CHATS_HIDE_STYLE if state.hide_past else PAST_CHATS_SHOW_STYLE
    with me.box(style=style):
        with me.box(
            style=me.Style(
                flex_direction="row",
                width="100%",
                padding=me.Padding(top="16px"),
                justify_content="space-between",
            )
        ):
            with me.content_button(
                on_click=on_show_hide, disabled=not state.past_conversations
            ):
                me.icon("menu")
            with me.content_button(
                on_click=on_start_new_conversation,
                disabled=not state.conversation.completed,
            ):
                me.icon("rate_review")
        if not state.hide_past:
            for conversation in state.past_conversations:
                with me.box(
                    key=conversation.id,  # they are GUIDs so should not clash with anything other on the page
                    on_click=select_past_conversation,
                    style=me.Style(
                        padding=me.Padding.all(16),
                        border_radius=16,
                    ),
                ):
                    me.text(text=conversation_display_title(conversation.title, 128))


def conversation_starter_box() -> None:
    with me.box(style=CHAT_STARTER_STYLE):
        header()
        with me.box(
            style=me.Style(
                width="min(680px, 100%)",
                # margin=me.Margin.symmetric(horizontal="auto", vertical=36),
            )
        ):
            me.text(
                "Enter a prompt to chat with FastAgency team",
                style=me.Style(font_size=20, margin=me.Margin(bottom=24)),
            )
            input_text(send_prompt, "prompt", disabled=False)


def send_prompt(prompt: str) -> Iterator[None]:
    ui = get_ui()
    wf = ui.app.wf

    name = wf.names[0]

    state = me.state(State)
    # me.navigate("/conversation")
    conversation = Conversation(
        title=prompt, completed=False, waiting_for_feedback=False
    )
    state.conversation = conversation
    state.in_conversation = True
    yield
    responses = send_prompt_to_autogen(prompt=prompt, wf=wf, name=name)
    yield from consume_responses(responses)


def conversation_box() -> None:
    state = me.state(State)
    conversation = state.conversation
    with me.box(style=CHAT_STARTER_STYLE):
        header()
        messages = conversation.messages
        with me.box(
            style=me.Style(overflow_y="auto", display="flex", flex_direction="column")
        ):
            me.box(
                key="conversationtop",
                style=me.Style(margin=me.Margin(bottom="1vh")),
            )
            for message in messages:
                message_box(message, conversation.is_from_the_past)
            if messages:
                me.box(
                    key="end_of_messages",
                    style=me.Style(margin=me.Margin(bottom="50vh")),
                )
