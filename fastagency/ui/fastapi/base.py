## IONats part

from collections.abc import Iterable, Mapping
from typing import Any, Callable, Optional, Union

from faststream import FastStream
from faststream.nats import NatsBroker

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
        fastapi_url: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        super_conversation: Optional["FastAPIProvider"] = None,
    ) -> None:
        """Provider for NATS.

        Args:
            wf (Workflows): The workflow object.
            fastapi_url (Optional[str], optional): The fastapi url. Defaults to None.
            user (Optional[str], optional): The user. Defaults to None.
            password (Optional[str], optional): The password. Defaults to None.
            super_conversation (Optional["FastAPIProvider"], optional): The super conversation. Defaults to None.
        """
        self.wf = wf

        self.user = user
        self.password = password

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

    def create_subconversation(self) -> "FastAPIProvider":
        return self

    @classmethod
    def Workflows(  # noqa: N802
        cls,
        nats_url: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Workflows:
        return FastAPIWorkflows(nats_url=nats_url, user=user, password=password)


class FastAPIWorkflows(Workflows):
    def __init__(
        self,
        nats_url: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """Initialize the fastapi workflows."""
        self._workflows: dict[
            str, tuple[Callable[[Workflows, UI, str, str], str], str]
        ] = {}

        self.nats_url = nats_url or "nats://localhost:4222"
        self.user = user
        self.password = password

        self.broker = NatsBroker(self.nats_url, user=self.user, password=self.password)
        self.app = FastStream(self.broker)

        self._initiate_chat_subject: str = "chat.server.initiate_chat"

        self.is_broker_running: bool = False

    def register(
        self, name: str, description: str, *, fail_on_redefintion: bool = False
    ) -> Callable[[Workflow], Workflow]:
        raise NotImplementedError("Just ignore this for now; @register")

    def run(self, name: str, session_id: str, ui: UI, initial_message: str) -> str:
        raise NotImplementedError("Just ignore this for now; @run")

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
