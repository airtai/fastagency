import re
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, fields
from typing import (
    Any,
    Callable,
    Literal,
    Optional,
    Protocol,
    Type,
    TypeVar,
    runtime_checkable,
)

__all__ = [
    "Chatable",
    "FunctionCallExecution",
    "IOMessage",
    "MessageType",
    "MultipleChoice",
    "SuggestedFunctionCall",
    "SystemMessage",
    "TextInput",
    "TextMessage",
    "Workflow",
    "WorkflowCompleted",
    "Workflows",
]

MessageType = Literal[
    "text_message",
    "suggested_function_call",
    "function_call_execution",
    "text_input",
    "multiple_choice",
    "system_message",
    "workflow_completed",
]


def _camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


@dataclass
class IOMessage(ABC):  # noqa: B024  # `IOMessage` is an abstract base class, but it has no abstract methods
    sender: Optional[str] = None
    recepient: Optional[str] = None
    # streaming: bool = False
    auto_reply: bool = False

    @property
    def type(self) -> MessageType:
        retval: MessageType = _camel_to_snake(self.__class__.__name__)  # type: ignore[assignment]
        return retval

    @staticmethod
    def _get_message_class(type: Optional[MessageType]) -> "Type[IOMessage]":
        type = type or "text_message"
        lookup: dict[MessageType, "Type[IOMessage]"] = {
            "text_message": TextMessage,
            "suggested_function_call": SuggestedFunctionCall,
            "function_call_execution": FunctionCallExecution,
            "text_input": TextInput,
            "multiple_choice": MultipleChoice,
            "system_message": SystemMessage,
            "workflow_completed": WorkflowCompleted,
        }
        return lookup[type]

    @staticmethod
    def create(type: Optional[MessageType] = None, **kwargs: Any) -> "IOMessage":
        cls = IOMessage._get_message_class(type)

        return cls(**kwargs)

    @staticmethod
    def _get_parameters_names() -> list[str]:
        return [field.name for field in fields(IOMessage)]

    def model_dump(self) -> dict[str, Any]:
        params_names = IOMessage._get_parameters_names()
        d = asdict(self)
        content = {k: v for k, v in d.items() if k not in params_names}
        retval = {k: v for k, v in d.items() if k in params_names}
        retval["content"] = content
        retval["type"] = self.type
        return retval


# message type that asks user something


@dataclass
class AskingMessage(IOMessage): ...


# type of output messages
@dataclass
class TextMessage(IOMessage):
    body: Optional[str] = None

    def __post_init__(self) -> None:
        """Set the default value for the `type` attribute."""
        if self.type is None:
            self.type = "text_message"


@dataclass
class SuggestedFunctionCall(IOMessage):
    function_name: Optional[str] = None
    call_id: Optional[str] = None
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class FunctionCallExecution(IOMessage):
    function_name: Optional[str] = None
    call_id: Optional[str] = None
    retval: Any = None


# types of input messages
@dataclass
class TextInput(AskingMessage):
    prompt: Optional[str] = None
    suggestions: list[str] = field(default_factory=list)
    password: bool = False


@dataclass
class MultipleChoice(AskingMessage):
    prompt: Optional[str] = None
    choices: list[str] = field(default_factory=list)
    default: Optional[str] = None
    single: bool = True
    # todo: add validation


@dataclass
class SystemMessage(IOMessage):
    message: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowCompleted(IOMessage):
    result: Optional[str] = None


class IOMessageVisitor(ABC):
    def visit(self, message: IOMessage) -> Optional[str]:
        method_name = f"visit_{message.type}"
        method = getattr(self, method_name, self.visit_default)
        return method(message)

    @abstractmethod
    def visit_default(self, message: IOMessage) -> Optional[str]: ...

    def visit_text_message(self, message: TextMessage) -> Optional[str]:
        return self.visit_default(message)

    def visit_suggested_function_call(
        self, message: SuggestedFunctionCall
    ) -> Optional[str]:
        return self.visit_default(message)

    def visit_function_call_execution(
        self, message: FunctionCallExecution
    ) -> Optional[str]:
        return self.visit_default(message)

    def visit_text_input(self, message: TextInput) -> Optional[str]:
        return self.visit_default(message)

    def visit_multiple_choice(self, message: MultipleChoice) -> Optional[str]:
        return self.visit_default(message)

    def visit_system_message(self, message: SystemMessage) -> Optional[str]:
        return self.visit_default(message)

    def visit_workflow_completed(self, message: WorkflowCompleted) -> Optional[str]:
        return self.visit_default(message)


# @dataclass
# class IOStreamingMessage:
#     chunk: str


@runtime_checkable
class Chatable(Protocol):
    def process_message(self, message: IOMessage) -> Optional[str]: ...

    # def process_streaming_message(
    #     self, message: IOStreamingMessage
    # ) -> Optional[str]: ...

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

    @property
    def names(self) -> list[str]: ...

    def get_description(self, name: str) -> str: ...
