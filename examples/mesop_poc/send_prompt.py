import mesop as me

from collections.abc import Iterable
from fastagency.core.base import IOMessage
from fastagency.core.mesop.base import MesopIO, run_workflow
from examples.mesop_poc.data_model import State

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
