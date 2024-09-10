from uuid import uuid4

import mesop as me

from ..data_model import Conversation, State


def header() -> None:
    def navigate_home(e: me.ClickEvent) -> None:
        me.navigate("/")

    with me.box(
        on_click=navigate_home,
        style=me.Style(
            cursor="pointer",
            padding=me.Padding.all(16),
        ),
    ):
        me.text(
            "FastAgency - Mesop",
            style=me.Style(
                font_weight=500,
                font_size=24,
                color="#3D3929",
                letter_spacing="0.3px",
            ),
        )


def conversation_completed() -> None:
    def start_new_conversation(ev: me.ClickEvent) -> None:
        state.in_conversation = False

    def save_and_start_new_conversation(ev: me.ClickEvent) -> None:
        state = me.state(State)
        conversation = state.conversation
        uuid: str = uuid4().hex
        becomme_past = Conversation(
            id=uuid,
            title=conversation.title,
            messages=conversation.messages,
            completed=True,
            is_from_the_past=True,
            waiting_for_feedback=False,
        )
        state.past_conversations.append(becomme_past)
        state.in_conversation = False

    state = me.state(State)
    with me.box(
        style=me.Style(
            cursor="pointer",
            padding=me.Padding.all(16),
        ),
    ):
        if not state.conversation.is_from_the_past:
            me.button(
                "Conversation with team has ended, save it and start a new one",
                on_click=save_and_start_new_conversation,
            )
        else:
            me.button(
                "Start a new conversation",
                on_click=start_new_conversation,
            )
