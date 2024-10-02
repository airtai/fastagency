import re
import textwrap
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Generator, Iterable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field, fields
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)

if TYPE_CHECKING:
    from fastagency.api.openapi import OpenAPI

__all__ = [
    "UI",
    "FunctionCallExecution",
    "IOMessage",
    "MessageType",
    "MultipleChoice",
    "Runnable",
    "SuggestedFunctionCall",
    "SystemMessage",
    "TextInput",
    "TextMessage",
    "Workflow",
    "WorkflowCompleted",
    "Workflows",
    "run_workflow",
]

MessageType = Literal[
    "text_message",
    "suggested_function_call",
    "function_call_execution",
    "text_input",
    "multiple_choice",
    "system_message",
    "workflow_completed",
    "error",
]


def _camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


@dataclass
class IOMessage(ABC):  # noqa: B024  # `IOMessage` is an abstract base class, but it has no abstract methods
    sender: Optional[str] = None
    recipient: Optional[str] = None
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
            "error": Error,
        }
        return lookup[type]

    @staticmethod
    def create(type: Optional[MessageType] = None, **kwargs: Any) -> "IOMessage":
        cls = IOMessage._get_message_class(type)

        content = kwargs.pop("content", {})
        kwargs.update(content)

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


@dataclass
class Error(IOMessage):
    short: Optional[str] = None
    long: Optional[str] = None


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

    def visit_error(self, message: Error) -> Optional[str]:
        return self.visit_default(message)


# @dataclass
# class IOStreamingMessage:
#     chunk: str


@runtime_checkable
class UI(Protocol):
    @contextmanager
    def create(self, app: "Runnable", import_string: str) -> Iterator[None]: ...

    def start(
        self,
        *,
        app: "Runnable",
        import_string: str,
        name: Optional[str] = None,
        initial_message: Optional[str] = None,
        single_run: bool = False,
    ) -> None: ...

    def process_message(self, message: IOMessage) -> Optional[str]: ...

    # def process_streaming_message(
    #     self, message: IOStreamingMessage
    # ) -> Optional[str]: ...

    def create_subconversation(self) -> "UI": ...


@runtime_checkable
class WSGI(Protocol):
    def handle_wsgi(
        self,
        app: "Runnable",
        environ: dict[str, Any],
        start_response: Callable[..., Any],
    ) -> list[bytes]: ...


@runtime_checkable
class ASGI(Protocol):
    async def handle_asgi(
        self,
        app: "Runnable",
        scope: dict[str, Any],
        receive: Callable[[dict[str, Any]], Awaitable[None]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None: ...


Workflow = TypeVar("Workflow", bound=Callable[["Workflows", UI, str, str], str])


Agent = TypeVar("Agent")


@runtime_checkable
class Workflows(Protocol):
    def register(
        self, name: str, description: str
    ) -> Callable[[Workflow], Workflow]: ...

    def run(self, name: str, session_id: str, ui: UI, initial_message: str) -> str: ...

    @property
    def names(self) -> list[str]: ...

    def get_description(self, name: str) -> str: ...

    def register_api(
        self,
        api: "OpenAPI",
        callers: Union[Agent, Iterable[Agent]],
        executors: Union[Agent, Iterable[Agent]],
        functions: Optional[
            Union[str, Iterable[Union[str, Mapping[str, Mapping[str, str]]]]]
        ] = None,
    ) -> None: ...


@runtime_checkable
class Runnable(Protocol):
    @contextmanager
    def create(self, import_string: str) -> Generator[None, None, None]: ...

    def start(
        self,
        *,
        import_string: str,
        name: Optional[str] = None,
        initial_message: Optional[str] = None,
        single_run: bool = False,
    ) -> None: ...

    @property
    def wf(self) -> Workflows: ...

    @property
    def ui(self) -> UI: ...

    @property
    def title(self) -> str: ...

    @property
    def description(self) -> str: ...


def run_workflow(
    *,
    wf: Workflows,
    ui: UI,
    name: Optional[str],
    initial_message: Optional[str] = None,
    single_run: bool = False,
) -> None:
    """Run a workflow.

    Args:
        wf (Workflows): The workflows object to use.
        ui (UI): The UI object to use.
        name (Optional[str]): The name of the workflow to run. If not provided, the default workflow will be run.
        initial_message (Optional[str], optional): The initial message to send to the workflow. If not provided, a default message will be sent. Defaults to None.
        single_run (bool, optional): If True, the workflow will only be run once. Defaults to False.
    """
    while True:
        name = wf.names[0] if name is None else name
        description = wf.get_description(name)

        if initial_message is None:
            initial_message = ui.process_message(
                TextInput(
                    sender="FastAgency",
                    recipient="user",
                    prompt=(
                        f"Starting a new workflow '{name}' with the following description:"
                        + "\n\n"
                        + f"{description}"
                        + "\n\nPlease enter an initial message"
                    ),
                )
            )
        else:
            ui.process_message(
                SystemMessage(
                    sender="FastAgency",
                    recipient="user",
                    message={
                        "body": (
                            f"Starting a new workflow '{name}' with the following description:"
                            + "\n\n"
                            + textwrap.indent(description, prefix=" " * 2)
                            + "\n\nand using the following initial message:"
                            + textwrap.indent(initial_message, prefix=" " * 2)
                        )
                    },
                )
            )

        result = wf.run(
            name=name,
            session_id="session_id",
            ui=ui.create_subconversation(),
            initial_message="Hi!" if initial_message is None else initial_message,
        )

        ui.process_message(
            WorkflowCompleted(
                sender="workflow",
                recipient="user",
                result=result,
            )
        )

        initial_message = None

        if single_run:
            break
