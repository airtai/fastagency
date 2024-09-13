from collections.abc import Iterator
from typing import Callable

import mesop as me

from ..data_model import State


def _on_blur(e: me.InputBlurEvent) -> None:
    state = me.state(State)
    setattr(state, e.key, e.value)


def input_user_feedback(
    send_feedback: Callable[[me.ClickEvent], Iterator[None]], disabled: bool = False
) -> None:
    def _on_feedback_blur(e: me.InputBlurEvent) -> None:
        state = me.state(State)
        state.conversation.feedback = e.value

    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
        )
    ):
        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                placeholder="Provide a feedback to the team",
                on_blur=_on_feedback_blur,
                disabled=disabled,
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
        with me.content_button(
            type="icon",
            on_click=send_feedback,
            disabled=disabled,
        ):
            me.icon("send")


def input_prompt(send_prompt: Callable[[me.ClickEvent], Iterator[None]]) -> None:
    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
        )
    ):
        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                placeholder="Enter a prompt",
                key="prompt",
                on_blur=_on_blur,
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
        with me.content_button(type="icon", on_click=send_prompt):
            me.icon("send")
