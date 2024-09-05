import mesop as me

from typing import Iterable, Optional
from fastagency.core.base import IOMessage
from fastagency.core.mesop.base import MesopIO, IOMessageVisitor, TextInput, TextMessage, MultipleChoice, run_workflow
from examples.mesop_poc.data_model import State, ConversationMessage

from examples.mesop_poc.workflows import wf

def send_prompt_to_autogen(prompt: str) -> Iterable[str]:
    #mesop_io = run_workflow(wf, "simple_learning", prompt)
    mesop_io = run_workflow(wf, "exam_practice", prompt)
    state = me.state(State)
    state.fastagency = mesop_io.id
    return mesop_io.get_message_stream()

def send_user_feedback_to_autogen(userResponse: str) -> Iterable[str]:
    state = me.state(State)
    mesopId = state.fastagency
    mesop_io = MesopIO.get_conversation(mesopId)
    mesop_io.respond(userResponse)
    return mesop_io.get_message_stream()


class MesopGUIMessageVisitor(IOMessageVisitor):
    def __init__(self, level, conversationId):
        self._level = level
        self._conversationId = conversationId

    def visit_default(self, message: IOMessage) -> None:
        return ConversationMessage(level=self._level, conversationId=self._conversationId
                                   , recipient=message.recepient, sender=message.sender, text="message")

    def visit_text_message(self, message: TextMessage) -> None:
        return ConversationMessage(level=self._level, conversationId=self._conversationId
                                   , recipient=message.recepient, sender=message.sender, text=message.body)

    def visit_text_input(self, message: TextInput) -> str:
        return ConversationMessage(level=self._level, conversationId=self._conversationId
                                   , recipient=message.recepient, sender=message.sender, text=message.prompt)

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        text = message.prompt + "\n" + "\n".join([f"{i+1}. {choice}" for i, choice in enumerate(message.choices)])

        return ConversationMessage(level=self._level, conversationId=self._conversationId
                                   , recipient=message.recepient, sender=message.sender, text=text)


    def process_message(self, message: IOMessage) -> Optional[str]:
        return self.visit(message)
