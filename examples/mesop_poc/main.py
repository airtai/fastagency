import mesop as me

from examples.mesop_poc.data_model import State, ChatMessage
from examples.mesop_poc.send_prompt import send_prompt_to_autogen, send_user_feedback_to_autogen
from examples.mesop_poc.fast_agency import Question
from examples.mesop_poc.styles import ROOT_BOX_STYLE, STYLESHEETS
from examples.mesop_poc.components.message import user_message, autogen_message
from examples.mesop_poc.components.common import header
from examples.mesop_poc.components.inputs import input_user_feedback, input_prompt


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
                "Enter a prompt to chat with Autogen team",
                style=me.Style(font_size=20, margin=me.Margin(bottom=24)),
            )
            input_prompt(send_prompt)


def send_prompt(e: me.ClickEvent):
    state = me.state(State)
    me.navigate("/conversation")
    prompt = state.prompt
    state.prompt = ""

    conversation = state.conversation
    messages = conversation.messages
    messages.append(ChatMessage(role="user", content=prompt))
    messages.append(ChatMessage(role="autogen", in_progress=True))
    yield

    me.scroll_into_view(key="end_of_messages")

    autogen_response = send_prompt_to_autogen(prompt)

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
                    autogen_message(message)
            if messages:
                me.box(
                    key="end_of_messages",
                    style=me.Style(
                        margin=me.Margin(
                            bottom="50vh" if messages[-1].in_progress else 0
                        )
                    ),
                )
        if state.waitingForInput:
            input_user_feedback(on_user_feedback)

def on_user_feedback(e: me.ClickEvent):
    state = me.state(State)
    feedback = state.feedback
    state.feedback = ""
    yield
    conversation = state.conversation
    messages = conversation.messages
    messages.append(ChatMessage(role="user", content=feedback))
    messages.append(ChatMessage(role="autogen", in_progress=True))
    yield

    me.scroll_into_view(key="end_of_messages")
    autogen_response = send_user_feedback_to_autogen(feedback)

    for chunk in autogen_response:
        if isinstance(chunk, Question):
            chunk = str(chunk)
        messages[-1].content += chunk
        yield

    messages[-1].in_progress = False
    yield
