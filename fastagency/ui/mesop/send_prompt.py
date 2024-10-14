from collections.abc import Iterable

import mesop as me

from ...base import ProviderProtocol
from ...logging import get_logger
from .data_model import State
from .mesop import MesopMessage, MesopUI, run_workflow_mesop

logger = get_logger(__name__)


def send_prompt_to_autogen(
    provider: ProviderProtocol, name: str
) -> Iterable[MesopMessage]:
    ui = run_workflow_mesop(provider, name=name)
    if not isinstance(ui.ui_base, MesopUI):  # pragma: no cover
        logger.error("")
        raise RuntimeError(f"Expected MesopUI, got {type(ui.ui_base)}")
    mesop_ui: MesopUI = ui.ui_base

    state = me.state(State)
    state.conversation.fastagency = ui.ui_base.id
    return mesop_ui.get_message_stream()


def send_user_feedback_to_autogen(user_response: str) -> Iterable[MesopMessage]:
    state = me.state(State)
    mesop_id = state.conversation.fastagency
    mesop_io = MesopUI.get_conversation(mesop_id)
    mesop_io.respond(user_response)
    return mesop_io.get_message_stream()


def get_more_messages() -> Iterable[MesopMessage]:
    state = me.state(State)
    mesop_id = state.conversation.fastagency
    mesop_io = MesopUI.get_conversation(mesop_id)
    return mesop_io.get_message_stream()
