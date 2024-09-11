import mesop as me

from .components.ui_common import darken_hex_color

ROOT_BOX_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    font_family="Inter",
    display="flex",
    flex_direction="row",
)

CHAT_STARTER_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    width="max(80%)",
    font_family="Inter",
    display="flex",
    flex_direction="column",
    padding=me.Padding.all(16),
)

PAST_CHATS_SHOW_STYLE = me.Style(
    background=darken_hex_color("#e7f2ff", 0.95),
    height="100%",
    width="min(300px)",
    font_family="Inter",
    display="flex",
    flex_direction="column",
)

PAST_CHATS_HIDE_STYLE = me.Style(
    background="#e7f2ff",
    height="10%",
    width="min(150px)",
    font_family="Inter",
    display="flex",
    flex_direction="column",
)

STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
]
