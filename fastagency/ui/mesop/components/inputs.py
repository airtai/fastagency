from collections.abc import Iterator
from typing import Callable, Optional

import mesop as me

from ....logging import get_logger
from ..data_model import State
from ..styles import MesopTextInputInnerStyles

# Get the logger
logger = get_logger(__name__)


def input_text(  # noqa: C901
    on_input: Callable[[str], Iterator[None]],
    *,
    key: str,
    disabled: bool = False,
    value: Optional[str] = None,
    style: MesopTextInputInnerStyles,
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
        if disabled or e.key != key_num:
            return
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
    key_num = f"{key}{len(state.conversation.messages)}"
    with me.box(style=style.box):
        if disabled:
            in_value = value
            key_num = f"{key}disabled{len(state.conversation.messages)}"
        else:
            input_key = get_input_key()
            in_value = getattr(state, input_key)
            key_num = f"{key}{len(state.conversation.messages)}"

        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                on_blur=on_blur,
                key=key_num,
                autosize=True,
                min_rows=3,
                max_rows=10,
                readonly=disabled,
                shortcuts={
                    me.Shortcut(key="enter", shift=True): on_newline,
                    me.Shortcut(key="enter"): on_submit,
                },
                style=style.native_textarea,
                value=in_value,
            )

        with me.content_button(
            type="icon",
            on_click=on_click,
            disabled=disabled,
        ):
            me.icon("send")
