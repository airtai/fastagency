"""The fastest way to bring multi-agent workflows to production."""

from .__about__ import __version__
from .app import FastAgency
from .base import UI, UIBase, WorkflowTypeVar, WorkflowsProtocol
from .messages import (
    FunctionCallExecution,
    IOMessage,
    MessageType,
    MultipleChoice,
    SuggestedFunctionCall,
    TextInput,
    TextMessage,
)

__all__ = [
    "UI",
    "FastAgency",
    "FunctionCallExecution",
    "IOMessage",
    "MessageType",
    "MultipleChoice",
    "SuggestedFunctionCall",
    "TextInput",
    "TextMessage",
    "UIBase",
    "WorkflowTypeVar",
    "WorkflowsProtocol",
    "__version__",
]
