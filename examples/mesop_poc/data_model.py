from dataclasses import dataclass, field
from typing import Literal, Optional
from uuid import UUID
import mesop as me
from fastagency.core.base import IOMessage


@dataclass(kw_only=True)
class ConversationMessage:
    level: int
    conversationId: UUID
    io_message: IOMessage

@dataclass
class Conversation:
    messages: list[ConversationMessage] = field(default_factory=list)

@me.stateclass
class State:
    conversationCompleted: bool = False
    waitingForFeedback: bool = False
    prompt: str = ""
    feedback: str = ""
    conversation: Conversation
    fastagency: Optional[UUID] = None
