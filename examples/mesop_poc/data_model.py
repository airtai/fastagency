from dataclasses import dataclass, field
from typing import Literal
from enum import Enum
from autogen.io.base import IOStream
import mesop as me

Role = Literal["user", "autogen"]

@dataclass(kw_only=True)
class ChatMessage:
    role: Role = "user"
    content: str = ""
    in_progress: bool = False

@dataclass
class Conversation:
    messages: list[ChatMessage] = field(default_factory=list)

@me.stateclass
class State:
    conversationCompleted: bool = False
    waitingForFeedback: bool = False
    prompt: str = ""
    feedback: str = ""
    conversation: Conversation
    autogen: int = -1
