import mesop as me

from .components.helpers import darken_hex_color

HEADER_BOX_STYLE = me.Style(
    padding=me.Padding(bottom="24px"),
)

HEADER_TEXT_STYLE = me.Style(
    font_weight=500,
    font_size=24,
    color="#3D3929",
    letter_spacing="0.3px",
)


ROOT_BOX_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    font_family="Inter",
    display="flex",
    flex_direction="row",
)

PAST_CHATS_SHOW_STYLE = me.Style(
    background=darken_hex_color("#e7f2ff", 0.98),
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

PAST_CHATS_INNER_STYLE = me.Style(
    flex_direction="row",
    width="100%",
    padding=me.Padding(top="16px"),
    justify_content="space-between",
)

PAST_CHATS_CONV_STYLE = (
    me.Style(
        padding=me.Padding.all(16),
        border_radius=16,
    ),
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

CONV_STARTER_STYLE = me.Style(
    width="min(680px, 100%)",
    # margin=me.Margin.symmetric(horizontal="auto", vertical=36),
)

CONV_STARTER_TEXT_STYLE = me.Style(font_size=20, margin=me.Margin(bottom=24))

CONV_LIST_STYLE = me.Style(overflow_y="auto", display="flex", flex_direction="column")

CONV_TOP_STYLE = me.Style(
    margin=me.Margin(bottom="1vh"),
)

CONV_MSG_STYLE = me.Style(margin=me.Margin(bottom="50vh"))

STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
]
