## IONats part

from collections.abc import AsyncIterator, Iterable, Mapping
from contextlib import asynccontextmanager
from typing import Any, Callable, Optional, Union

import uvicorn
from fastapi import FastAPI

from fastagency.logging import get_logger

from ...base import (
    UI,
    Agent,
    IOMessage,
    IOMessageVisitor,
    Workflow,
    Workflows,
)

logger = get_logger(__name__)


class FastAPIProvider(IOMessageVisitor):
    def __init__(
        self,
        wf: Workflows,
        *,
        host: str = "localhost",
        port: int = 8000,
        user: Optional[str] = None,
        password: Optional[str] = None,
        super_conversation: Optional["FastAPIProvider"] = None,
    ) -> None:
        """Provider for NATS.

        Args:
            wf (Workflows): The workflow object.
            host (str, optional): The host. Defaults to "localhost".
            port (int, optional): The port. Defaults to 8000.
            user (Optional[str], optional): The user. Defaults to None.
            password (Optional[str], optional): The password. Defaults to None.
            super_conversation (Optional["FastAPIProvider"], optional): The super conversation. Defaults to None.
        """
        self.wf = wf

        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.app = FastAPI()

    def visit(self, message: IOMessage) -> Optional[str]:
        method_name = f"visit_{message.type}"
        method = getattr(self, method_name, self.visit_default)
        return method(message)

    def process_message(self, message: IOMessage) -> Optional[str]:
        try:
            return self.visit(message)
        except Exception as e:
            logger.error(f"Error in process_message: {e}", stack_info=True)
            raise

    @asynccontextmanager
    async def lifespan(self, app: Any) -> AsyncIterator[None]:
        config = uvicorn.Config(
            self.app, host=self.host, port=self.port, log_level="info"
        )
        server = uvicorn.Server(config)

        await server.startup()
        try:
            yield
        finally:
            await server.shutdown()

    def create_subconversation(self) -> "FastAPIProvider":
        return self

    @classmethod
    def Workflows(  # noqa: N802
        cls,
        host: str = "localhost",
        port: int = 8000,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Workflows:
        return FastAPIWorkflows(host=host, port=port, user=user, password=password)


class FastAPIWorkflows(Workflows):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """Initialize the fastapi workflows."""
        self._workflows: dict[
            str, tuple[Callable[[Workflows, UI, str, str], str], str]
        ] = {}

        self.user = user
        self.password = password

        self.is_broker_running: bool = False

    def register(
        self, name: str, description: str, *, fail_on_redefintion: bool = False
    ) -> Callable[[Workflow], Workflow]:
        raise NotImplementedError("Just ignore this for now; @register")

    def run(self, name: str, session_id: str, ui: UI, initial_message: str) -> str:
        raise NotImplementedError("Need to implement this; @run")

    @property
    def names(self) -> list[str]:
        return ["simple_learning"]

    def get_description(self, name: str) -> str:
        return "Student and teacher learning chat"

    def register_api(
        self,
        api: Any,
        callers: Union[Agent, Iterable[Agent]],
        executors: Union[Agent, Iterable[Agent]],
        functions: Optional[
            Union[str, Iterable[Union[str, Mapping[str, Mapping[str, str]]]]]
        ] = None,
    ) -> None:
        raise NotImplementedError(
            "Just ignore this for now, will be removed from this protocol; @register_api"
        )
