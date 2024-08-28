import mesop as me
from examples.mesop_poc.data_model import State


def header():
    def navigate_home(e: me.ClickEvent):
        me.navigate("/")
        state = me.state(State)

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

def conversation_completed():
    def navigate_home(e: me.ClickEvent):
        me.navigate("/")
        state = me.state(State)

    with me.box(
        style=me.Style(
            cursor="pointer",
            padding=me.Padding.all(16),
        ),
    ):
        me.button(
            "Conversation with team has ended, start a new one",
            on_click=navigate_home,
        )
