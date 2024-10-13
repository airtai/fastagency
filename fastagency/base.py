import inspect
from collections.abc import Awaitable, Generator, Iterable, Iterator, Mapping
from contextlib import contextmanager
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

from .logging import get_logger
from .messages import IOMessage, MessageProcessorProtocol

if TYPE_CHECKING:
    from fastagency.api.openapi import OpenAPI

__all__ = [
    "UIBase",
    "WSGIProtocol",
    "ASGIProtocol",
    "ProviderProtocol",
    "WorkflowsProtocol",
    "AdapterProtocol",
    "Runnable",
    "Workflow",
    "Agent",
]

logger = get_logger(__name__)


@runtime_checkable
class UIBase(MessageProcessorProtocol, Protocol):
    @contextmanager
    def create(self, app: "Runnable", import_string: str) -> Iterator[None]: ...

    def start(
        self,
        *,
        app: "Runnable",
        import_string: str,
        name: Optional[str] = None,
        params: dict[str, Any],
        single_run: bool = False,
    ) -> None: ...

    def create_workflow_ui(self, workflow_uuid: str) -> "UI": ...

    # def process_streaming_message(
    #     self, message: IOStreamingMessage
    # ) -> Optional[str]: ...


class CreateWorkflowUIMixin:
    def create_workflow_ui(self: UIBase, workflow_uuid: str) -> "UI":
        return UI(uibase=self, workflow_uuid=workflow_uuid)


class UI:
    def __init__(self, uibase: UIBase, workflow_uuid: str) -> None:
        if workflow_uuid is None:
            logger.error("workflow_uuid must be provided")
            raise ValueError("workflow_uuid must be provided")
        self._ui_base = uibase
        self._workflow_uuid = workflow_uuid

    @property
    def workflow_uuid(self) -> str:
        return self._workflow_uuid

    @property
    def ui_base(self) -> UIBase:
        return self._ui_base

    def process_message(self, message: IOMessage) -> Optional[str]:
        return self._ui_base.process_message(message)

    def text_message(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # text_message specific parameters
        body: Optional[str] = None,
    ) -> Optional[str]:
        return self._ui_base.text_message(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            body=body,
        )

    def suggested_function_call(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # suggested_function_call specific parameters
        function_name: Optional[str] = None,
        call_id: Optional[str] = None,
        arguments: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        return self._ui_base.suggested_function_call(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            function_name=function_name,
            call_id=call_id,
            arguments=arguments,
        )

    def function_call_execution(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # function_call_execution specific parameters
        function_name: Optional[str] = None,
        call_id: Optional[str] = None,
        retval: Any = None,
    ) -> Optional[str]:
        return self._ui_base.function_call_execution(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            function_name=function_name,
            call_id=call_id,
            retval=retval,
        )

    def text_input(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # text_input specific parameters
        prompt: Optional[str] = None,
        suggestions: Optional[list[str]] = None,
        password: bool = False,
    ) -> Optional[str]:
        return self._ui_base.text_input(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            prompt=prompt,
            suggestions=suggestions,
            password=password,
        )

    def multiple_choice(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # multiple_choice specific parameters
        prompt: Optional[str] = None,
        choices: Optional[list[str]] = None,
        default: Optional[str] = None,
        single: bool = True,
    ) -> Optional[str]:
        return self._ui_base.multiple_choice(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            prompt=prompt,
            choices=choices,
            default=default,
            single=single,
        )

    def system_message(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # system_message specific parameters
        message: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        return self._ui_base.system_message(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            message=message,
        )

    def workflow_started(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # workflow_started specific parameters
        name: Optional[str] = None,
        description: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        return self._ui_base.workflow_started(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            name=name,
            description=description,
            params=params,
        )

    def workflow_completed(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # workflow_completed specific parameters
        result: Optional[str] = None,
    ) -> Optional[str]:
        return self._ui_base.workflow_completed(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            result=result,
        )

    def error(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        # error specific parameters
        short: Optional[str] = None,
        long: Optional[str] = None,
    ) -> Optional[str]:
        return self._ui_base.error(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            short=short,
            long=long,
        )

    def keep_alive(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
    ) -> Optional[str]:
        return self._ui_base.keep_alive(
            workflow_uuid=self.workflow_uuid,
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
        )


@runtime_checkable
class WSGIProtocol(Protocol):
    def handle_wsgi(
        self,
        app: "Runnable",
        environ: dict[str, Any],
        start_response: Callable[..., Any],
    ) -> list[bytes]: ...


@runtime_checkable
class ASGIProtocol(Protocol):
    async def handle_asgi(
        self,
        app: "Runnable",
        scope: dict[str, Any],
        receive: Callable[[dict[str, Any]], Awaitable[None]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None: ...


# signature of a function decorated with @wf.register
Workflow = TypeVar("Workflow", bound=Callable[[UI, dict[str, Any]], str])


Agent = TypeVar("Agent")


@runtime_checkable
class ProviderProtocol(Protocol):
    def run(
        self,
        name: str,
        ui: UI,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> str: ...

    """Run a workflow.

    Creates a new workflow and assigns it workflow_uuid. Then it calls the
    workflow function (function decorated with @wf.register) with the given
    ui and workflow_uuid.

    Args:
        name (str): The name of the workflow to run.
        ui (UI): The UI object to use.
        **kwargs: Additional parameters to pass to the workflow function.
    """

    @property
    def names(self) -> list[str]: ...

    def get_description(self, name: str) -> str: ...


@runtime_checkable
class WorkflowsProtocol(ProviderProtocol, Protocol):
    def register(
        self, name: str, description: str
    ) -> Callable[[Workflow], Workflow]: ...

    def register_api(
        self,
        api: "OpenAPI",
        callers: Union[Agent, Iterable[Agent]],
        executors: Union[Agent, Iterable[Agent]],
        functions: Optional[
            Union[str, Iterable[Union[str, Mapping[str, Mapping[str, str]]]]]
        ] = None,
    ) -> None: ...


def check_register_decorator(func: Workflow) -> None:
    # get names of all parameters in the function signature
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    if params != ["ui", "params"]:
        raise ValueError(
            f"Expected function signature to be 'def func(ui: UI, workflow_uuid: str, params: dict[str, Any]) -> str', got {sig}"
        )


@runtime_checkable
class AdapterProtocol(Protocol):
    @classmethod
    def create_provider(*args: Any, **kwargs: Any) -> ProviderProtocol: ...


@runtime_checkable
class Runnable(Protocol):
    @contextmanager
    def create(self, import_string: str) -> Generator[None, None, None]: ...

    def start(
        self,
        *,
        import_string: str,
        name: Optional[str] = None,
        params: dict[str, Any],
        single_run: bool = False,
    ) -> None: ...

    @property
    def provider(self) -> ProviderProtocol: ...

    @property
    def ui(self) -> UIBase: ...

    @property
    def title(self) -> str: ...

    @property
    def description(self) -> str: ...
