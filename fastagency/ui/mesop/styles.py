from dataclasses import dataclass, field

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

PAST_CHATS_CONV_STYLE = me.Style(
    padding=me.Padding.all(16),
    border_radius=16,
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

CONV_STARTER_WF_BOX_STYLE = me.Style(
    display="flex", flex_direction="row", justify_content="flex-start"
)

CONV_LIST_STYLE = me.Style(
    overflow_y="auto",
    display="flex",
    flex_direction="column",
    padding=me.Padding.symmetric(horizontal=16),
)

CONV_TOP_STYLE = me.Style(
    margin=me.Margin(bottom="1vh"),
)

CONV_MSG_STYLE = me.Style(margin=me.Margin(bottom="50vh"))

STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
]

FIREBASE_STYLESHEETS = [
    "https://www.gstatic.com/firebasejs/ui/6.1.0/firebase-ui-auth.css"
]

MSG_DEFAULT_HEADER_MD_STYLE = me.Style(
    padding=me.Padding(top=8, right=16, left=16, bottom=8)
)
MSG_DEFAULT_HEADER_BOX_STYLE = me.Style(
    background="#ddd",
    padding=me.Padding.all(0),
    border_radius=8,
)

MSG_DEFAULT_BOX_STYLE = me.Style(
    background="#fff",
    border_radius=8,
    margin=me.Margin.symmetric(vertical=16),
)

MSG_DEFAULT_MD_STYLE = me.Style(padding=me.Padding.all(16))
MSG_DEFAULT_MD_SCROLABLE_STYLE = me.Style(
    padding=me.Padding(top=16, left=16, right=16),
    overflow_y="auto",
    max_height="300px",
    margin=me.Margin(bottom=16),
)

MSG_SYSTEM_HEADER_BOX_STYLE = me.Style(
    background="#b3e5fc",
    padding=me.Padding.all(0),
    border_radius=8,
)

MSG_SUGESTED_FUNCTION_CALL_HEADER_BOX_STYLE = me.Style(
    background="#fff0b2",
    padding=me.Padding.all(0),
    border_radius=8,
)

MSG_FUNCTION_CALL_EXECUTION_HEADER_BOX_STYLE = me.Style(
    background="#ffccbc",
    padding=me.Padding.all(0),
    border_radius=8,
)

MSG_ERROR_HEADER_BOX_STYLE = me.Style(
    background="#f44336",
    padding=me.Padding.all(0),
    border_radius=8,
)

MSG_ERROR_HEADER_MD_STYLE = me.Style(
    padding=me.Padding(top=8, right=16, left=16, bottom=8),
    color="#fff",
)

MSG_TEXT_INPUT_HEADER_BOX_STYLE = me.Style(
    background="#e6ee9c",
    padding=me.Padding.all(0),
    border_radius=8,
)

MSG_TEXT_INPUT_MD_STYLE = me.Style(
    background="#e0e0e0",
    padding=me.Padding.all(16),
)

MSG_DEFAULT_BUTTON_STYLE = me.Style(
    margin=me.Margin.symmetric(horizontal=8),
    padding=me.Padding.all(16),
    border_radius=8,
    background="#1976d2",
)

MSG_DEFAULT_SELECTED_BUTTON_STYLE = me.Style(
    margin=me.Margin.symmetric(horizontal=8),
    padding=me.Padding.all(16),
    border_radius=8,
    background="#1976d2",
    color="#fff",
)

MSG_DEFAULT_DISABLED_BUTTON_STYLE = me.Style(
    margin=me.Margin.symmetric(horizontal=8),
    padding=me.Padding.all(16),
    border_radius=8,
    background="#64b5f6",
    color="#fff",
)


@dataclass
class MesopMessageStyles:
    box: me.Style = field(default_factory=lambda: MSG_DEFAULT_BOX_STYLE)
    md: me.Style = field(default_factory=lambda: MSG_DEFAULT_MD_STYLE)
    scrollable_md: me.Style = field(
        default_factory=lambda: MSG_DEFAULT_MD_SCROLABLE_STYLE
    )
    header_box: me.Style = field(default_factory=lambda: MSG_DEFAULT_HEADER_BOX_STYLE)
    header_md: me.Style = field(default_factory=lambda: MSG_DEFAULT_HEADER_MD_STYLE)
    button: me.Style = field(default_factory=lambda: MSG_DEFAULT_BUTTON_STYLE)
    disabled_button: me.Style = field(
        default_factory=lambda: MSG_DEFAULT_DISABLED_BUTTON_STYLE
    )
    selected_button: me.Style = field(
        default_factory=lambda: MSG_DEFAULT_SELECTED_BUTTON_STYLE
    )


TEXT_INPUT_INNER_BOX_STYLE = me.Style(
    border_radius=8,
    padding=me.Padding.all(16),
    background="white",
    display="flex",
    width="100%",
)

TEXT_INPUT_NATIVE_TEXTAREA_STYLE = me.Style(
    padding=me.Padding(top=16, left=16),
    # outline="none",
    width="100%",
    border=me.Border.all(me.BorderSide(style="none")),
    background="#e1f5fe",
)

SINGLE_CHOICE_RADIO_STYLE = me.Style(
    display="flex", flex_direction="column", padding=me.Padding.all(16)
)

SINGLE_CHOICE_BOX_STYLE = me.Style(
    display="flex",
    flex_direction="row",
    padding=me.Padding(left=8, right=8, top=0, bottom=16),
)

SINGLE_CHOICE_BUTTON_STYLE = me.Style(
    margin=me.Margin.symmetric(horizontal=8),
    padding=me.Padding.all(16),
    border_radius=8,
    background="#1976d2",
)

SINGLE_CHOICE_SELECTED_BUTTON_STYLE = me.Style(
    margin=me.Margin.symmetric(horizontal=8),
    padding=me.Padding.all(16),
    border_radius=8,
    background="#1976d2",
    color="#fff",
)

SINGLE_CHOICE_DISABLED_BUTTON_STYLE = me.Style(
    margin=me.Margin.symmetric(horizontal=8),
    padding=me.Padding.all(16),
    border_radius=8,
    background="#64b5f6",
    color="#fff",
)

MULTIPLE_CHOICE_RADIO_STYLE = me.Style(
    display="flex",
    flex_direction="column",
    padding=me.Padding.all(16),
)

MULTIPLE_CHOICE_BUTTON_STYLE = me.Style(
    margin=me.Margin(top=16), border_radius=8, background="#1976d2"
)

MULTIPLE_CHOICE_CHECKBOX_STYLE = me.Style()

LOGIN_BOX_STYLE = me.Style(display="flex", justify_content="center")

LOGIN_BTN_BOX_STYLE = me.Style(text_align="center", margin=me.Margin(top=100))
LOGOUT_BTN_BOX_STYLE = me.Style(position="absolute", top="16px", right="16px")


@dataclass
class MesopTextInputInnerStyles:
    box: me.Style = field(default_factory=lambda: TEXT_INPUT_INNER_BOX_STYLE)
    native_textarea: me.Style = field(
        default_factory=lambda: TEXT_INPUT_NATIVE_TEXTAREA_STYLE
    )


@dataclass
class MesopSingleChoiceInnerStyles:
    # radio: me.Style = field(default_factory=lambda: SINGLE_CHOICE_RADIO_STYLE)
    box: me.Style = field(default_factory=lambda: SINGLE_CHOICE_BOX_STYLE)
    button: me.Style = field(default_factory=lambda: SINGLE_CHOICE_BUTTON_STYLE)
    disabled_button: me.Style = field(
        default_factory=lambda: SINGLE_CHOICE_DISABLED_BUTTON_STYLE
    )
    selected_button: me.Style = field(
        default_factory=lambda: SINGLE_CHOICE_SELECTED_BUTTON_STYLE
    )


@dataclass
class MesopMultipleChoiceInnerStyles:
    box: me.Style = field(default_factory=lambda: MULTIPLE_CHOICE_RADIO_STYLE)
    checkbox: me.Style = field(default_factory=lambda: MULTIPLE_CHOICE_CHECKBOX_STYLE)
    button: me.Style = field(default_factory=lambda: MULTIPLE_CHOICE_BUTTON_STYLE)


@dataclass
class MesopMessagesStyles:
    default: MesopMessageStyles = field(default_factory=lambda: MesopMessageStyles())

    error: MesopMessageStyles = field(
        default_factory=lambda: MesopMessageStyles(
            header_box=MSG_ERROR_HEADER_BOX_STYLE,
            header_md=MSG_ERROR_HEADER_MD_STYLE,
        )
    )

    system: MesopMessageStyles = field(
        default_factory=lambda: MesopMessageStyles(
            header_box=MSG_SYSTEM_HEADER_BOX_STYLE,
        )
    )

    text: MesopMessageStyles = field(default_factory=lambda: MesopMessageStyles())

    suggested_function_call: MesopMessageStyles = field(
        default_factory=lambda: MesopMessageStyles(
            header_box=MSG_SUGESTED_FUNCTION_CALL_HEADER_BOX_STYLE,
        )
    )

    function_call_execution: MesopMessageStyles = field(
        default_factory=lambda: MesopMessageStyles(
            header_box=MSG_FUNCTION_CALL_EXECUTION_HEADER_BOX_STYLE,
        )
    )

    text_input: MesopMessageStyles = field(
        default_factory=lambda: MesopMessageStyles(
            header_box=MSG_TEXT_INPUT_HEADER_BOX_STYLE,
        )
    )

    text_input_inner: MesopTextInputInnerStyles = field(
        default_factory=lambda: MesopTextInputInnerStyles()
    )

    single_choice_inner: MesopSingleChoiceInnerStyles = field(
        default_factory=lambda: MesopSingleChoiceInnerStyles()
    )

    multiple_choice_inner: MesopMultipleChoiceInnerStyles = field(
        default_factory=lambda: MesopMultipleChoiceInnerStyles()
    )


@dataclass
class MesopHomePageStyles:
    chat_starter: me.Style = field(default_factory=lambda: CHAT_STARTER_STYLE)
    conv_list: me.Style = field(default_factory=lambda: CONV_LIST_STYLE)
    conv_msg: me.Style = field(default_factory=lambda: CONV_MSG_STYLE)
    conv_top: me.Style = field(default_factory=lambda: CONV_TOP_STYLE)
    conv_starter: me.Style = field(default_factory=lambda: CONV_STARTER_STYLE)
    conv_starter_text: me.Style = field(default_factory=lambda: CONV_STARTER_TEXT_STYLE)
    conv_starter_wf_box: me.Style = field(
        default_factory=lambda: CONV_STARTER_WF_BOX_STYLE
    )
    header: me.Style = field(default_factory=lambda: HEADER_BOX_STYLE)
    header_text: me.Style = field(default_factory=lambda: HEADER_TEXT_STYLE)
    past_chats_hide: me.Style = field(default_factory=lambda: PAST_CHATS_HIDE_STYLE)
    past_chats_show: me.Style = field(default_factory=lambda: PAST_CHATS_SHOW_STYLE)
    past_chats_inner: me.Style = field(default_factory=lambda: PAST_CHATS_INNER_STYLE)
    past_chats_conv: me.Style = field(default_factory=lambda: PAST_CHATS_CONV_STYLE)
    root: me.Style = field(default_factory=lambda: ROOT_BOX_STYLE)
    stylesheets: list[str] = field(default_factory=lambda: STYLESHEETS)
    firebase_stylesheets: list[str] = field(
        default_factory=lambda: FIREBASE_STYLESHEETS
    )
    message: MesopMessagesStyles = field(default_factory=lambda: MesopMessagesStyles())
    login_box: me.Style = field(default_factory=lambda: LOGIN_BOX_STYLE)
    login_btn_container: me.Style = field(default_factory=lambda: LOGIN_BTN_BOX_STYLE)
    logout_btn_container: me.Style = field(default_factory=lambda: LOGOUT_BTN_BOX_STYLE)
