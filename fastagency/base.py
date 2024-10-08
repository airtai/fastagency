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
from uuid import UUID, uuid4

from .messages import (
    MessageProcessorProtocol,
    WorkflowCompleted,
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


Workflow = TypeVar("Workflow", bound=Callable[[UI, UUID], str])


Agent = TypeVar("Agent")


@runtime_checkable
class ProviderProtocol(Protocol):
    def run(
        self, name: str, ui: UI, workflow_uuid: Optional[UUID] = None, **kwargs: Any
    ) -> str: ...

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
    single_run: bool = False,
    **kwargs: Any,
) -> None:
    """Run a workflow.

    Args:
        provider (ProviderProtocol): The provider to use.
        ui (UI): The UI object to use.
        name (Optional[str]): The name of the workflow to run. If not provided, the default workflow will be run.
        single_run (bool, optional): If True, the workflow will only be run once. Defaults to False.
        **kwargs: The parameters to pass to the workflow.
    """
    while True:
        name = provider.names[0] if name is None else name
        description = provider.get_description(name)
        workflow_uuid = uuid4()

        ui.workflow_started(
            name=name,
            description=description,
            workflow_uuid=workflow_uuid,
            params=kwargs,
        )
        result = provider.run(
            name=name,
            session_id="session_id",
            ui=ui,
        )

        ui.process_message(
            WorkflowCompleted(
                sender="workflow",
                recipient="user",
                result=result,
            )
        )

        if single_run:
            break
