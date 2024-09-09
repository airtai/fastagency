from dataclasses import dataclass, field
from typing import Optional

import mesop as me


@dataclass
class Conversation:
    title: str = ""
    # messages: list[ConversationMessage] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)


@me.stateclass
class State:
    conversation_completed: bool = False
    waiting_for_feedback: bool = False
    prompt: str = ""
    feedback: str = ""
    conversation: Conversation
    past_conversations: list[Conversation] = field(default_factory=list)
    fastagency: Optional[str] = None
