from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)

__all__ = [
    "Chatable",
    "FunctionCallExecutionContent",
    "IOMessage",
    "IOStreamingMessage",
    "MessageContent",
    "MessageType",
    "MultipleChoiceContent",
    "IOMessage",
    "SuggestedFunctionCallContent",
    "TextInputContent",
    "TextMessageContent",
    "Workflow",
    "Workflows",
]


# type of input messages
@dataclass
class TextMessageContent:
    body: Optional[str] = None


@dataclass
class SuggestedFunctionCallContent:
    function_name: str
    call_id: str
    arguments: Dict[str, Any]


@dataclass
class FunctionCallExecutionContent:
    function_name: str
    call_id: str
    retval: Any


# types of output messages
@dataclass
class TextInputContent:
    prompt: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)
    password: bool = False


@dataclass
class MultipleChoiceContent:
    prompt: Optional[str]
    choices: List[str]
    default: Optional[str] = None
    single: bool = True


MessageContent = Union[
    TextMessageContent,
    SuggestedFunctionCallContent,
    FunctionCallExecutionContent,
    TextInputContent,
    MultipleChoiceContent,
]

MessageContentTypes = Union[
    Type[TextMessageContent],
    Type[SuggestedFunctionCallContent],
    Type[FunctionCallExecutionContent],
    Type[TextInputContent],
    Type[MultipleChoiceContent],
]

MessageType = Literal[
    "text_message",
    "suggested_function_call",
    "function_call_execution",
    "text_input",
    "multiple_choice",
]


def _get_message_class(type: MessageType) -> MessageContentTypes:
    lookup: Dict[MessageType, MessageContentTypes] = {
        "text_message": TextMessageContent,
        "suggested_function_call": SuggestedFunctionCallContent,
        "function_call_execution": FunctionCallExecutionContent,
        "text_input": TextInputContent,
        "multiple_choice": MultipleChoiceContent,
    }
    return lookup[type]


@dataclass
class IOMessage:
    type: MessageType = "text_message"
    content: MessageContent = None  # type: ignore[assignment] # (fixed in __post_init__)
    sender: Optional[str] = None
    recepient: Optional[str] = None
    heading: Optional[str] = None
    streaming: bool = False

    @classmethod
    def from_dict(cls, **kwargs: Any) -> "IOMessage":
        type = kwargs.get("type", "text_message")
        content_dict = kwargs.get("content", {})
        content_cls = _get_message_class(type)
        content = content_cls(**content_dict)
        kwargs["type"] = type
        kwargs["content"] = content

        return IOMessage(**kwargs)

    def __post_init__(self) -> None:
        """Create content object if content is a dict."""
        content = self.content if self.content is not None else {}
        if not isinstance(content, _get_message_class(self.type)):
            if isinstance(content, dict):
                self.content = _get_message_class(self.type)(**content)
            else:  # pragma: no cover
                raise ValueError(
                    f"Invalid content type for message of type {self.type}: {content}"
                )


class IOStreamingMessage:
    chunk: str


@runtime_checkable
class Chatable(Protocol):
    def process_message(self, message: IOMessage) -> Optional[str]: ...

    def process_streaming_message(
        self, message: IOStreamingMessage
    ) -> Optional[str]: ...

    def create_subconversation(self) -> "Chatable": ...


Workflow = TypeVar("Workflow", bound=Callable[[Chatable, str, str], str])


@runtime_checkable
class Workflows(Protocol):
    def register(
        self, name: str, description: str
    ) -> Callable[[Workflow], Workflow]: ...

    def run(
        self, name: str, session_id: str, io: Chatable, initial_message: str
    ) -> str: ...
