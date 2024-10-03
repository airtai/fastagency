## IONats part

from collections.abc import Iterable, Mapping
from typing import Any, Callable, Optional, Union
from uuid import UUID, uuid4

import nats
from fastapi import APIRouter
from pydantic import BaseModel

from fastagency.logging import get_logger

from ...base import (
    UI,
    Agent,
    IOMessage,
    IOMessageVisitor,
    Workflow,
    Workflows,
)
from ..nats import InitiateModel, NatsWorkflows

logger = get_logger(__name__)


class FastAPIProvider(IOMessageVisitor):
    def __init__(
        self,
        wf: NatsWorkflows,
        *,
        user: Optional[str] = None,
        password: Optional[str] = None,
        super_conversation: Optional["FastAPIProvider"] = None,
    ) -> None:
        """Provider for NATS.

        Args:
            wf (Workflows): The workflow object.
            user (Optional[str], optional): The user. Defaults to None.
            password (Optional[str], optional): The password. Defaults to None.
            super_conversation (Optional["FastAPIProvider"], optional): The super conversation. Defaults to None.
        """
        self.wf = wf

        self.user = user
        self.password = password

        self.router = self.setup_routes()

    def setup_routes(self) -> APIRouter:
        router = APIRouter()

        class WorkflowInfo(BaseModel):
            name: str
            description: str

        @router.post("/initiate_chat")
        async def initiate_chat(
            workflow_name: str,
            # user_id: UUID,
            # conversation_id: UUID,
            msg: str,
        ) -> InitiateModel:
            user_id: UUID = uuid4()
            conversation_id: UUID = uuid4()
            init_msg = InitiateModel(
                user_id=user_id,
                conversation_id=conversation_id,
                msg=msg,
            )

            nc = await nats.connect(
                self.wf.nats_url, user=self.wf.user, password=self.wf.password
            )
            await nc.publish(
                "chat.server.initiate_chat",
                init_msg.model_dump_json().encode(),
            )

            return init_msg

        @router.get("/discover")
        async def discover() -> list[WorkflowInfo]:
            names = self.wf.names
            descriptions = [self.wf.get_description(name) for name in names]
            return [
                WorkflowInfo(name=name, description=description)
                for name, description in zip(names, descriptions)
            ]

        return router

    def visit_default(self, message: IOMessage) -> Optional[str]:
        raise NotImplementedError(f"visit_{message.type}")

    def process_message(self, message: IOMessage) -> Optional[str]:
        try:
            return self.visit(message)
        except Exception as e:
            logger.error(f"Error in process_message: {e}", stack_info=True)
            raise

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
