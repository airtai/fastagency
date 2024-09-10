from dataclasses import dataclass, field
from typing import Optional

import mesop as me


@dataclass
class Conversation:
    id: str = ""
    title: str = ""
    completed: bool = False
    waiting_for_feedback: bool = False
    feedback: str = ""
    # messages: list[ConversationMessage] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    fastagency: Optional[str] = None


@me.stateclass
class State:
    in_conversation: bool = False  # True when in active conversation, or past one.
    prompt: str = ""
    conversation: Conversation
    past_conversations: list[Conversation] = field(default_factory=list)
    fastagency: Optional[str] = None
