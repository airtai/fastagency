"""The fastest way to bring multi-agent workflows to production."""

from .__about__ import __version__
from .app import FastAgency
from .base import (
    UI,
    FunctionCallExecution,
    IOMessage,
    MessageType,
    MultipleChoice,
    SuggestedFunctionCall,
    TextInput,
    TextMessage,
    Workflow,
    WorkflowsProtocol,
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
    "WorkflowsProtocol",
    "Workflow",
    "__version__",
]
