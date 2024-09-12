"""The fastest way to bring multi-agent workflows to production."""

from .__about__ import __version__
from .app import FastAgency
from .base import (
    Chatable,
    FunctionCallExecution,
    IOMessage,
    MessageType,
    MultipleChoice,
    SuggestedFunctionCall,
    TextInput,
    TextMessage,
    Workflow,
    Workflows,
)

__all__ = [
    "Chatable",
    "FastAgency",
    "FunctionCallExecution",
    "IOMessage",
    "MessageType",
    "MultipleChoice",
    "SuggestedFunctionCall",
    "TextInput",
    "TextMessage",
    "Workflows",
    "Workflow",
    "__version__",
]
