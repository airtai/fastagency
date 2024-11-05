from dataclasses import dataclass, field
from typing import Optional

import mesop as me


@dataclass
class ConversationMessage:
    io_message_json: str = ""
    level: int = 0
    conversation_id: str = ""
    feedback: list[str] = field(default_factory=list)
    feedback_completed: bool = False


@dataclass
class Conversation:
    id: str = ""
    title: str = ""
    completed: bool = False
    waiting_for_feedback: bool = False
    feedback: str = ""
    is_from_the_past: bool = False
    messages: list[ConversationMessage] = field(default_factory=list)
    fastagency: Optional[str] = None


@me.stateclass
class State:
    in_conversation: bool = False  # True when in active conversation, or past one.
    prompt_input: str = ""
    prompt_output: str = ""
    conversation: Conversation
    past_conversations: list[Conversation] = field(default_factory=list)
    hide_past: bool = True
    available_workflows: list[str] = field(default_factory=list)
    available_workflows_initialized = False
    available_workflows_exception = False
    authenticated_user: Optional[str] = None
