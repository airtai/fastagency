import mesop as me
import json
from examples.mesop_poc.data_model import State
from fastagency.core.mesop.send_prompt import send_prompt_to_autogen, send_user_feedback_to_autogen
from fastagency.core.mesop.styles import ROOT_BOX_STYLE, STYLESHEETS
from fastagency.core.mesop.message import message_box
from fastagency.core.mesop.components.ui_common import header, conversation_completed
from fastagency.core.mesop.components.inputs import input_user_feedback, input_prompt
from fastagency.core.mesop.base import MesopMessage, AskingMessage, WorkflowCompleted

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

def _handle_message(state: State, message:MesopMessage ):
    messages = state.conversation.messages
    level = message.conversation.level
    conversationId = message.conversation.id
    io_message = message.io_message
    message_dict = io_message.model_dump()
    message_string = json.dumps({"level": level, "conversationId": conversationId, "io_message": message_dict})
    messages.append(message_string)
    state.conversation.messages = list(messages)
    if isinstance(io_message, AskingMessage):
        state.waitingForFeedback = True
        state.conversationCompleted = False
    if isinstance(io_message, WorkflowCompleted):
        state.conversationCompleted = True
        state.waitingForFeedback = False

def send_prompt(e: me.ClickEvent):
    state = me.state(State)
    me.navigate("/conversation")
    prompt = state.prompt
    state.prompt = ""
    state.conversationCompleted = False
    state.waitingForFeedback = False
    yield
    me.scroll_into_view(key="end_of_messages")
    yield
    responses = send_prompt_to_autogen(prompt)
    for message in responses:
        state = me.state(State)
        _handle_message(state, message)
        yield
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
            for message in messages:
                message_box(message)
            if messages:
                me.box(
                    key="end_of_messages",
                    style=me.Style(
                        margin=me.Margin(
                            bottom="50vh"
                        )
                    ),
                )
        if state.waitingForFeedback:
            input_user_feedback(on_user_feedback)
        if state.conversationCompleted:
            conversation_completed(reset_conversation)

def reset_conversation():
    state = me.state(State)
    state.conversationCompleted = False
    state.conversation.messages = []
    state.waitingForFeedback = False
    state.autogen = -1
    state.prompt = ""
    state.feedback = ""

def on_user_feedback(e: me.ClickEvent):
    state = me.state(State)
    feedback = state.feedback
    state.waitingForFeedback = False
    yield
    state.feedback = ""
    state.waitingForFeedback = False
    yield
    me.scroll_into_view(key="end_of_messages")
    yield
    responses = send_user_feedback_to_autogen(feedback)
    for message in responses:
        state = me.state(State)
        _handle_message(state, message)
        yield
    yield
