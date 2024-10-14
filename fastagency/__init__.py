"""The fastest way to bring multi-agent workflows to production."""

from .__about__ import __version__
from .app import FastAgency
from .base import UI, UIBase, Workflow, WorkflowsProtocol
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
    "UIBase",
    "FastAgency",
    "FunctionCallExecution",
    "IOMessage",
    "MessageType",
    "MultipleChoice",
    "SuggestedFunctionCall",
    "TextInput",
    "TextMessage",
    "WorkflowsProtocol",
    "Workflow",
    "UI",
    "__version__",
]
