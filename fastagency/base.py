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
    TextInput,
    WorkflowCompleted,
    WorkflowStarted,
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
        initial_message: Optional[str] = None,
        single_run: bool = False,
    ) -> None: ...

    # def process_streaming_message(
    #     self, message: IOStreamingMessage
    # ) -> Optional[str]: ...

    def create_subconversation(self) -> "UI": ...


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
# Workflow = TypeVar("Workflow", bound=Callable[["WorkflowsProtocol", UI, str, str], str])
# parameters are: WorkflowsProtocol, UI, workflow_uuid, params (kwargs)
Workflow = TypeVar("Workflow", bound=Callable[[UI, str, dict[str, Any]], str])


Agent = TypeVar("Agent")


@runtime_checkable
class ProviderProtocol(Protocol):
    # def run(self, name: str, session_id: str, ui: UI, initial_message: str) -> str: ...
    def run(self, name: str, ui: UI, **kwargs: Any) -> str: ...

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
        initial_message: Optional[str] = None,
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
    name: Optional[str],
    initial_message: Optional[str] = None,
    single_run: bool = False,
) -> None:
    """Run a workflow.

    Args:
        provider (ProviderProtocol): The provider to use.
        ui (UI): The UI object to use.
        name (Optional[str]): The name of the workflow to run. If not provided, the default workflow will be run.
        initial_message (Optional[str], optional): The initial message to send to the workflow. If not provided, a default message will be sent. Defaults to None.
        single_run (bool, optional): If True, the workflow will only be run once. Defaults to False.
    """
    while True:
        name = provider.names[0] if name is None else name
        description = provider.get_description(name)

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
                WorkflowStarted(
                    sender="FastAgency",
                    recipient="user",
                    name=name,
                    description=description,
                    params={"initial_message": initial_message},
                )
            )

        result = provider.run(
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
