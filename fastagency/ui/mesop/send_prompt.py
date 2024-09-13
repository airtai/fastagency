from collections.abc import Iterable

import mesop as me

from ...base import Workflows
from .base import MesopMessage, MesopUI, run_workflow
from .data_model import State


def send_prompt_to_autogen(
    prompt: str, wf: Workflows, name: str
) -> Iterable[MesopMessage]:
    mesop_io = run_workflow(wf, name=name, initial_message=prompt)
    state = me.state(State)
    state.conversation.fastagency = mesop_io.id
    return mesop_io.get_message_stream()


def send_user_feedback_to_autogen(user_response: str) -> Iterable[MesopMessage]:
    state = me.state(State)
    mesop_id = state.conversation.fastagency
    mesop_io = MesopUI.get_conversation(mesop_id)
    mesop_io.respond(user_response)
    return mesop_io.get_message_stream()
