import mesop as me

from examples.mesop_poc.data_model import State, ChatMessage
from examples.mesop_poc.send_prompt import send_prompt_autogen, send_user_response_to_autogen
from examples.mesop_poc.fast_agency import Question


ROOT_BOX_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    font_family="Inter",
    display="flex",
    flex_direction="column",
)

STYLESHEETS = [
  "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
]

SECURITY_POLICY = me.SecurityPolicy(
    allowed_iframe_parents=["https://huggingface.co"]
)


@me.page(
    path="/",
    stylesheets=STYLESHEETS,
    security_policy=SECURITY_POLICY,
)
def home_page():
    with me.box(style=ROOT_BOX_STYLE):
        header()
        with me.box(
            style=me.Style(
                width="min(680px, 100%)",
                margin=me.Margin.symmetric(horizontal="auto", vertical=36),
            )
        ):
            me.text(
                "Enter a prompt to chat with Autogen",
                style=me.Style(font_size=20, margin=me.Margin(bottom=24)),
            )
            # Uncomment this in the next step:

            chat_input()

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
            "Autogen chat",
            style=me.Style(
                font_weight=500,
                font_size=24,
                color="#3D3929",
                letter_spacing="0.3px",
            ),
        )

def user_input():
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
        if state.waitingForInput:
            with me.box(style=me.Style(flex_grow=1)):
                me.native_textarea(
                    value=state.input,
                    placeholder="Enter a prompt",
                    on_blur=on_blur,
                    style=me.Style(
                        padding=me.Padding(top=16, left=16),
                        outline="none",
                        width="100%",
                        border=me.Border.all(me.BorderSide(style="none")),
                    ),
                )
            with me.content_button(
                type="icon", on_click=send_input
            ):
                me.icon("send")

def chat_input():
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
                value=state.input,
                placeholder="Enter a prompt",
                on_blur=on_blur,
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


def on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.input = e.value

def send_input(e: me.ClickEvent):
    state = me.state(State)
    print("send input")
    input = state.input
    state.input = ""
    conversation = state.conversation
    messages = conversation.messages
    messages.append(ChatMessage(role="user", content=input))
    messages.append(ChatMessage(role="model", in_progress=True))
    yield

    me.scroll_into_view(key="end_of_messages")

    print("xx sending user response state je", state.autogen)
    autogen_response = send_user_response_to_autogen(input)

    for chunk in autogen_response:
        if isinstance(chunk, Question):
            chunk = str(chunk)
        messages[-1].content += chunk
        yield
    messages[-1].in_progress = False
    yield


def send_prompt(e: me.ClickEvent):
    state = me.state(State)
    print("send prompt")
    me.navigate("/conversation")
    input = state.input
    state.input = ""

    conversation = state.conversation
    messages = conversation.messages
    history = messages[:]
    messages.append(ChatMessage(role="user", content=input))
    messages.append(ChatMessage(role="model", in_progress=True))
    yield

    me.scroll_into_view(key="end_of_messages")

    autogen_response = send_prompt_autogen(input, history)

    for chunk in autogen_response:
        if isinstance(chunk, Question):
            chunk = str(chunk)
        messages[-1].content += chunk
        yield
    messages[-1].in_progress = False
    yield


@me.page(path="/conversation", stylesheets=STYLESHEETS, security_policy=SECURITY_POLICY)
def conversation_page():
    state = me.state(State)
    with me.box(style=ROOT_BOX_STYLE):
        header()
        user_input()
        messages = state.conversation.messages
        with me.box(
            style=me.Style(
                overflow_y="auto",
            )
        ):
            me.text("Autogen: ", style=me.Style(font_weight=500))

            for message in messages:
                if message.role == "user":
                    user_message(message.content)
                else:
                    model_message(message)
            if messages:
                me.box(
                    key="end_of_messages",
                    style=me.Style(
                        margin=me.Margin(
                            bottom="50vh" if messages[-1].in_progress else 0
                        )
                    ),
                )


def user_message(content: str):
    with me.box(
        style=me.Style(
            background="#e7f2ff",
            padding=me.Padding.all(16),
            margin=me.Margin.symmetric(vertical=16),
            border_radius=16,
        )
    ):
        me.text(content)

def model_message(message: ChatMessage):
    with me.box(
        style=me.Style(
            background="#fff",
            padding=me.Padding.all(16),
            border_radius=16,
            margin=me.Margin.symmetric(vertical=16),
        )
    ):
        me.markdown(message.content)
        if message.in_progress:
            me.progress_spinner()
