import re
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, fields
from typing import Any, Literal, Optional, Protocol, Type
from uuid import UUID, uuid4

from pydantic import BaseModel

from .logging import get_logger

__all__ = [
    "IOMessage",
    "TextMessage",
    "SuggestedFunctionCall",
    "FunctionCallExecution",
    "TextInput",
    "MultipleChoice",
    "SystemMessage",
    "KeepAlive",
    "WorkflowStarted",
    "WorkflowCompleted",
    "Error",
    "MessageType",
    "MessageProcessorProtocol",
    "MessageProcessorMixin",
]


logger = get_logger(__name__)


def _camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


# we keep this hardcoded for mypy and type checks
MessageType = Literal[
    "text_message",
    "suggested_function_call",
    "function_call_execution",
    "text_input",
    "multiple_choice",
    "system_message",
    "keep_alive",
    "workflow_started",
    "workflow_completed",
    "error",
]


@dataclass
class IOMessage(
    ABC
):  # `IOMessage` is an abstract base class, but it has no abstract methods
    workflow_uuid: str
    sender: Optional[str] = None
    recipient: Optional[str] = None
    auto_reply: bool = False
    uuid: str = field(default_factory=lambda: str(uuid4().hex))

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
            "keep_alive": KeepAlive,
            "system_message": SystemMessage,
            "workflow_started": WorkflowStarted,
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
class WorkflowStarted(IOMessage):
    name: Optional[str] = None
    description: Optional[str] = None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowCompleted(IOMessage):
    result: Optional[str] = None


@dataclass
class Error(IOMessage):
    short: Optional[str] = None
    long: Optional[str] = None


@dataclass
class KeepAlive(IOMessage): ...


class MessageProcessorProtocol(Protocol):
    def process_message(self, message: IOMessage) -> Optional[str]: ...

    def text_message(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # text_message specific parameters
        body: Optional[str] = None,
    ) -> Optional[str]: ...

    def suggested_function_call(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # suggested_function_call specific parameters
        function_name: Optional[str] = None,
        call_id: Optional[str] = None,
        arguments: Optional[dict[str, Any]] = None,
    ) -> Optional[str]: ...

    def function_call_execution(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # function_call_execution specific parameters
        function_name: Optional[str] = None,
        call_id: Optional[str] = None,
        retval: Any = None,
    ) -> Optional[str]: ...

    def text_input(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # text_input specific parameters
        prompt: Optional[str] = None,
        suggestions: Optional[list[str]] = None,
        password: bool = False,
    ) -> Optional[str]: ...

    def multiple_choice(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # multiple_choice specific parameters
        prompt: Optional[str] = None,
        choices: Optional[list[str]] = None,
        default: Optional[str] = None,
        single: bool = True,
    ) -> Optional[str]: ...

    def system_message(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # system_message specific parameters
        message: Optional[dict[str, Any]] = None,
    ) -> Optional[str]: ...

    def workflow_started(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # workflow_started specific parameters
        name: Optional[str] = None,
        description: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[str]: ...

    def workflow_completed(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # workflow_completed specific parameters
        result: Optional[str] = None,
    ) -> Optional[str]: ...

    def error(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # error specific parameters
        short: Optional[str] = None,
        long: Optional[str] = None,
    ) -> Optional[str]: ...

    def keep_alive(
        self,
        # common parameters for all messages
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
    ) -> Optional[str]: ...


class MessageProcessorMixin(ABC):
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

    def visit_keep_alive(self, message: KeepAlive) -> Optional[str]:
        return self.visit_default(message)

    def visit_workflow_started(self, message: WorkflowStarted) -> Optional[str]:
        return self.visit_default(message)

    def visit_workflow_completed(self, message: WorkflowCompleted) -> Optional[str]:
        return self.visit_default(message)

    def visit_error(self, message: Error) -> Optional[str]:
        return self.visit_default(message)

    def process_message(self, message: IOMessage) -> Optional[str]:
        try:
            return self.visit(message)
        except Exception as e:
            # log the error and return None
            logger.error(f"Error processing message ({message}): {e}", exc_info=True)
            return None

    def text_message(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        body: Optional[str] = None,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        return self.process_message(
            TextMessage(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                body=body,
            )
        )

    def suggested_function_call(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        function_name: Optional[str] = None,
        call_id: Optional[str] = None,
        arguments: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        arguments = arguments or {}
        return self.process_message(
            SuggestedFunctionCall(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                function_name=function_name,
                call_id=call_id,
                arguments=arguments,
            )
        )

    def function_call_execution(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        function_name: Optional[str] = None,
        call_id: Optional[str] = None,
        retval: Any = None,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        return self.process_message(
            FunctionCallExecution(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                function_name=function_name,
                call_id=call_id,
                retval=retval,
            )
        )

    def text_input(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        prompt: Optional[str] = None,
        suggestions: Optional[list[str]] = None,
        password: bool = False,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        suggestions = suggestions or []
        return self.process_message(
            TextInput(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                prompt=prompt,
                suggestions=suggestions,
                password=password,
            )
        )

    def multiple_choice(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        prompt: Optional[str] = None,
        choices: Optional[list[str]] = None,
        default: Optional[str] = None,
        single: bool = True,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        choices = choices or []
        return self.process_message(
            MultipleChoice(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                prompt=prompt,
                choices=choices,
                default=default,
                single=single,
            )
        )

    def system_message(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        message: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        message = message or {}
        return self.process_message(
            SystemMessage(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                message=message,
            )
        )

    def workflow_started(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        params = params or {}
        return self.process_message(
            WorkflowStarted(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                name=name,
                description=description,
                params=params,
            )
        )

    def workflow_completed(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        result: Optional[str] = None,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        return self.process_message(
            WorkflowCompleted(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                result=result,
            )
        )

    def error(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        short: Optional[str] = None,
        long: Optional[str] = None,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        return self.process_message(
            Error(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
                short=short,
                long=long,
            )
        )

    def keep_alive(
        self,
        workflow_uuid: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
    ) -> Optional[str]:
        uuid = uuid or str(uuid4().hex)
        return self.process_message(
            KeepAlive(
                sender=sender,
                recipient=recipient,
                auto_reply=auto_reply,
                uuid=uuid,
                workflow_uuid=workflow_uuid,
            )
        )


class InputResponseModel(BaseModel):
    msg: str
    question_uuid: Optional[UUID] = None
    error: bool = False


class InitiateWorkflowModel(BaseModel):
    user_id: Optional[str] = None
    workflow_uuid: UUID
    name: str
    params: dict[str, Any]
