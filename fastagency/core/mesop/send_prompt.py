from collections.abc import Iterable

import mesop as me

from examples.mesop_poc.data_model import State
from examples.mesop_poc.workflows import wf
from fastagency.core.mesop.base import MesopIO, MesopMessage, run_workflow


def send_prompt_to_autogen(prompt: str) -> Iterable[MesopMessage]:
    # mesop_io = run_workflow(wf, "simple_learning", prompt)
    mesop_io = run_workflow(wf, "exam_practice", prompt)
    state = me.state(State)
    state.fastagency = mesop_io.id
    return mesop_io.get_message_stream()


def send_user_feedback_to_autogen(user_response: str) -> Iterable[MesopMessage]:
    state = me.state(State)
    mesop_id = state.fastagency
    mesop_io = MesopIO.get_conversation(mesop_id)
    mesop_io.respond(user_response)
    return mesop_io.get_message_stream()
