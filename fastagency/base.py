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

from .messages import (
    MessageProcessorProtocol,
)

if TYPE_CHECKING:
    from fastagency.api.openapi import OpenAPI

__all__ = [
    "UI",
    "WSGIProtocol",
    "ASGIProtocol",
    "ProviderProtocol",
    "WorkflowsProtocol",
    "AdapterProtocol",
    "Runnable",
    "Workflow",
    "Agent",
    "run_workflow",
]


@runtime_checkable
class UI(MessageProcessorProtocol, Protocol):
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

    def create_workflow_ui(self, workflow_uuid: str) -> "WorkflowUI": ...

    # def process_streaming_message(
    #     self, message: IOStreamingMessage
    # ) -> Optional[str]: ...


class CreateWorkflowUIMixin:
    def create_workflow_ui(self: UI, workflow_uuid: str) -> "WorkflowUI":
        return WorkflowUI(ui=self, workflow_uuid=workflow_uuid)


class WorkflowUI:
    def __init__(self, ui: UI, workflow_uuid: str) -> None:
        self.ui = ui
        self.workflow_uuid = workflow_uuid

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
        return self.ui.text_message(
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
        return self.ui.suggested_function_call(
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
        workflow_uuid: Optional[str] = None,
        # function_call_execution specific parameters
        function_name: Optional[str] = None,
        call_id: Optional[str] = None,
        retval: Any = None,
    ) -> Optional[str]:
        return self.ui.function_call_execution(
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            workflow_uuid=workflow_uuid,
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
        workflow_uuid: Optional[str] = None,
        # text_input specific parameters
        prompt: Optional[str] = None,
        suggestions: Optional[list[str]] = None,
        password: bool = False,
    ) -> Optional[str]:
        return self.ui.text_input(
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
        return self.ui.multiple_choice(
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
        workflow_uuid: Optional[str] = None,
        # system_message specific parameters
        message: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        return self.ui.system_message(
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            workflow_uuid=workflow_uuid,
            message=message,
        )

    def workflow_started(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        workflow_uuid: Optional[str] = None,
        # workflow_started specific parameters
        name: Optional[str] = None,
        description: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        return self.ui.workflow_started(
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            workflow_uuid=workflow_uuid,
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
        workflow_uuid: Optional[str] = None,
        # workflow_completed specific parameters
        result: Optional[str] = None,
    ) -> Optional[str]:
        return self.ui.workflow_completed(
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            workflow_uuid=workflow_uuid,
            result=result,
        )

    def error(
        self,
        # common parameters for all messages
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        auto_reply: bool = False,
        uuid: Optional[str] = None,
        workflow_uuid: Optional[str] = None,
        # error specific parameters
        short: Optional[str] = None,
        long: Optional[str] = None,
    ) -> Optional[str]:
        return self.ui.error(
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            workflow_uuid=workflow_uuid,
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
        workflow_uuid: Optional[str] = None,
    ) -> Optional[str]:
        return self.ui.keep_alive(
            sender=sender,
            recipient=recipient,
            auto_reply=auto_reply,
            uuid=uuid,
            workflow_uuid=workflow_uuid,
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
Workflow = TypeVar("Workflow", bound=Callable[[WorkflowUI, dict[str, Any]], str])


Agent = TypeVar("Agent")


@runtime_checkable
class ProviderProtocol(Protocol):
    def run(
        self,
        name: str,
        ui: WorkflowUI,
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
    def ui(self) -> UI: ...

    @property
    def title(self) -> str: ...

    @property
    def description(self) -> str: ...


def run_workflow(
    *,
    provider: ProviderProtocol,
    ui: UI,
    workflow_uuid: str,
    name: Optional[str],
    params: dict[str, Any],
    single_run: bool = False,
) -> None:
    """Run a workflow.

    Args:
        provider (ProviderProtocol): The provider to use.
        ui (UI): The UI object to use.
        workflow_uuid (str): The UUID of the workflow.
        name (Optional[str]): The name of the workflow to run. If not provided, the default workflow will be run.
        params (dict[str, Any]): Additional parameters to pass to the workflow function.
        single_run (bool, optional): If True, the workflow will only be run once. Defaults to False.
    """
    while True:
        name = provider.names[0] if name is None else name
        description = provider.get_description(name)

        wfui = ui.create_workflow_ui(workflow_uuid)

        wfui.workflow_started(
            sender="FastAgency",
            recipient="user",
            name=name,
            description=description,
            params=params,
        )

        result = provider.run(
            name,
            wfui,
            **params,
        )

        wfui.workflow_completed(
            sender="workflow",
            recipient="user",
            result=result,
        )

        if single_run:
            break
