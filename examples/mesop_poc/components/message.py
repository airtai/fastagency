import mesop as me
from examples.mesop_poc.data_model import ConversationMessage

def message_box(message: ConversationMessage):
    with me.box(
        style=me.Style(
            background="#fff",
            padding=me.Padding.all(16),
            border_radius=16,
            margin=me.Margin.symmetric(vertical=16),
        )
    ):
        message_text = str(message.io_message).json()
        me.markdown(message_text)

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

#def autogen_message(message: ChatMessage):
#    with me.box(
#        style=me.Style(
#            background="#fff",
#            padding=me.Padding.all(16),
#            border_radius=16,
#            margin=me.Margin.symmetric(vertical=16),
#        )
#    ):
#        me.markdown(message.content)
#        if message.in_progress:
#            me.progress_spinner()
