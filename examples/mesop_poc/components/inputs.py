import mesop as me
from examples.mesop_poc.data_model import State

def _on_user_feedback_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.feedback = e.value


def input_user_feedback(send_feedback):
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
                on_blur=_on_user_feedback_blur,
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
        with me.content_button(
            type="icon", on_click=send_feedback
        ):
            me.icon("send")


def _on_prompt_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.prompt = e.value


def input_prompt(send_prompt):
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
        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                placeholder="Enter a prompt",
                on_blur=_on_prompt_blur,
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
        with me.content_button(
            type="icon", on_click=send_prompt
        ):
            me.icon("send")
