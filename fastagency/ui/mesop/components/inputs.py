from collections.abc import Iterator
from typing import Callable, Optional

import mesop as me

from ..data_model import State


def input_text(
    on_input: Callable[[str], Iterator[None]],
    key: str,
    disabled: bool = False,
    value: Optional[str] = None,
) -> None:
    def on_click(e: me.ClickEvent) -> Iterator[None]:
        state = me.state(State)
        output_key = get_output_key()
        inp = getattr(state, output_key)
        clear_in_out()
        yield from on_input(inp)

    def on_newline(e: me.TextareaShortcutEvent) -> Iterator[None]:
        state = me.state(State)
        input_key = get_input_key()
        setattr(state, input_key, e.value + "\n")
        yield

    def on_submit(e: me.TextareaShortcutEvent) -> Iterator[None]:
        clear_in_out()
        yield from on_input(e.value)

    def on_blur(e: me.InputBlurEvent) -> None:
        state = me.state(State)
        input_key, output_key = get_in_out_keys()
        setattr(state, input_key, e.value)
        setattr(state, output_key, e.value)

    def get_input_key() -> str:
        return f"{key}_input"

    def get_output_key() -> str:
        return f"{key}_output"

    def get_in_out_keys() -> list[str]:
        return [get_input_key(), get_output_key()]

    def clear_in_out() -> None:
        input_key, output_key = get_in_out_keys()
        setattr(state, input_key, "")
        setattr(state, output_key, "")

    state = me.state(State)
    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
        )
    ):
        if disabled:
            in_value = value
        else:
            input_key = get_input_key()
            in_value = getattr(state, input_key)

        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                on_blur=on_blur,
                key=key,
                autosize=True,
                min_rows=3,
                max_rows=10,
                readonly=disabled,
                shortcuts={
                    me.Shortcut(key="enter", shift=True): on_newline,
                    me.Shortcut(key="enter"): on_submit,
                },
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
                value=in_value,
            )
            me.focus_component(key=key)

        with me.content_button(
            type="icon",
            on_click=on_click,
            disabled=disabled,
        ):
            me.icon("send")


def _on_blur(e: me.InputBlurEvent) -> None:
    state = me.state(State)
    setattr(state, e.key, e.value)


def input_user_feedback(
    send_feedback: Callable[[me.ClickEvent], Iterator[None]],
    disabled: bool = False,
    value: Optional[str] = None,
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
        optional_value = {"value": value} if value is not None else {}

        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                placeholder="Provide a feedback to the team",
                on_blur=_on_feedback_blur,
                readonly=disabled,
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
                **optional_value,
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
