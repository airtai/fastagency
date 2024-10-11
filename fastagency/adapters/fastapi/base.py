## IONats part

import asyncio
import json
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Callable, Optional
from uuid import UUID, uuid4

import requests
import websockets
from asyncer import asyncify, syncify
from fastapi import APIRouter, WebSocket
from pydantic import BaseModel

from fastagency.logging import get_logger

from ...base import UI, ProviderProtocol, Runnable, WorkflowsProtocol
from ...messages import (
    AskingMessage,
    IOMessage,
    MessageProcessorMixin,
)
from ..nats import InitiateWorkflowModel, InputResponseModel

logger = get_logger(__name__)


class InititateChatModel(BaseModel):
    workflow_name: str
    workflow_uuid: str
    user_id: Optional[str]
    params: dict[str, Any]


class WorkflowInfo(BaseModel):
    name: str
    description: str


class FastAPIAdapter(MessageProcessorMixin):
    def __init__(
        self,
        provider: ProviderProtocol,
        *,
        user: Optional[str] = None,
        password: Optional[str] = None,
        # super_conversation: Optional["FastAPIAdapter"] = None,
        initiate_workflow_path: str = "/fastagency/initiate_workflow",
        discovery_path: str = "/fastagency/discovery",
        ws_path: str = "/fastagency/ws",
    ) -> None:
        """Provider for FastAPI.

        Args:
            provider (ProviderProtocol): The provider.
            user (Optional[str], optional): The user. Defaults to None.
            password (Optional[str], optional): The password. Defaults to None.
            super_conversation (Optional["FastAPIProvider"], optional): The super conversation. Defaults to None.
            initiate_workflow_path (str, optional): The initiate workflow path. Defaults to "/fastagency/initiate_workflow".
            discovery_path (str, optional): The discovery path. Defaults to "/fastagency/discovery".
            ws_path (str, optional): The websocket path. Defaults to "/fastagency/ws".
        """
        self.provider = provider

        self.user = user
        self.password = password

        self.router = self.setup_routes()

        self.initiate_chat_path = initiate_workflow_path
        self.discovery_path = discovery_path
        self.ws_path = ws_path

        self.websockets: dict[str, WebSocket] = {}

    def setup_routes(self) -> APIRouter:
        router = APIRouter()

        @router.post(self.initiate_chat_path)
        async def initiate_chat(
            initiate_chat: InititateChatModel,
        ) -> InitiateWorkflowModel:
            user_id: UUID = uuid4()
            workflow_uuid: UUID = uuid4()

            init_msg = InitiateWorkflowModel(
                user_id=user_id,
                workflow_uuid=workflow_uuid,
                params=initiate_chat.params,
                name=initiate_chat.workflow_name,
            )

            return init_msg

        @router.websocket(self.ws_path)
        async def websocket_endpoint(websocket: WebSocket) -> None:
            await websocket.accept()
            init_msg_json = await websocket.receive_text()
            init_msg = InitiateWorkflowModel.model_validate_json(init_msg_json)

            self.websockets["workflow_uuid"] = websocket

            try:
                await asyncify(self.provider.run)(
                    name=init_msg.name,
                    ui=self,
                    workflow_uuid=init_msg.workflow_uuid.hex,
                    user_id=init_msg.user_id.hex,
                    **init_msg.params,
                )
            except Exception as e:
                logger.warning(f"Error in websocket_endpoint: {e}", stack_info=True)
            finally:
                self.websockets.pop("workflow_uuid")

        @router.get(self.discovery_path)
        def discovery() -> list[WorkflowInfo]:
            names = self.provider.names
            descriptions = [self.provider.get_description(name) for name in names]
            return [
                WorkflowInfo(name=name, description=description)
                for name, description in zip(names, descriptions)
            ]

        return router

    def visit_default(self, message: IOMessage) -> Optional[str]:
        async def a_visit_default(
            self: FastAPIAdapter, message: IOMessage
        ) -> Optional[str]:
            workflow_uuid = message.workflow_uuid
            websocket = self.websockets[workflow_uuid]  # type: ignore[index]
            await websocket.send_text(json.dumps(message.model_dump()))

            if isinstance(message, AskingMessage):
                return await websocket.receive_text()
            return None

        return syncify(a_visit_default)(self, message)

    # def process_message(self, message: IOMessage) -> Optional[str]:
    #     try:
    #         return self.visit(message)
    #     except Exception as e:
    #         logger.error(f"Error in process_message: {e}", stack_info=True)
    #         raise

    def create_subconversation(self) -> UI:
        return self

    @contextmanager
    def create(self, app: Runnable, import_string: str) -> Iterator[None]:
        raise NotImplementedError("create")

    def start(
        self,
        *,
        app: "Runnable",
        import_string: str,
        name: Optional[str] = None,
        params: dict[str, Any],
        single_run: bool = False,
    ) -> None:
        raise NotImplementedError("start")

    @classmethod
    def create_provider(
        cls,
        fastapi_url: str,
        fastapi_user: Optional[str] = None,
        fastapi_password: Optional[str] = None,
        nats_url: Optional[str] = None,
        nats_user: Optional[str] = None,
        nats_password: Optional[str] = None,
    ) -> ProviderProtocol:
        return FastAPIProvider(
            fastapi_url=fastapi_url,
            # fastapi_user=fastapi_user,
            # fastapi_password=fastapi_password,
            # nats_url=nats_url,
            # nats_user=nats_user,
            # nats_password=nats_password,
        )


class FastAPIProvider(ProviderProtocol):
    def __init__(
        self,
        fastapi_url: str,
        # fastapi_user: Optional[str] = None,
        # fastapi_password: Optional[str] = None,
        # nats_url: Optional[str] = None,
        # nats_user: Optional[str] = None,
        # nats_password: Optional[str] = None,
        initiate_chat_path: str = "/fastagency/initiate_chat",
        discovery_path: str = "/fastagency/discovery",
        ws_path: str = "/fastagency/ws",
        # todo: we need security context
    ) -> None:
        """Initialize the fastapi workflows."""
        self._workflows: dict[
            str, tuple[Callable[[WorkflowsProtocol, UI, str, str], str], str]
        ] = {}

        self.fastapi_url = (
            fastapi_url[:-1] if fastapi_url.endswith("/") else fastapi_url
        )
        # self.fastapi_user = fastapi_user
        # self.fastapi_password = fastapi_password

        # # self.nats_url = nats_url or "ws://localhost:9222"
        # if not self.nats_url.startswith(
        #     "ws://"  # nosemgrep
        # ) and not self.nats_url.startswith("wss://"):
        #     raise ValueError(
        #         f"NATS URL must start with ws:// or wss:// but got {self.nats_url}"  # nosemgrep
        #     )
        # self.nats_user = nats_user
        # self.nats_password = nats_password

        self.is_broker_running: bool = False

        self.initiate_chat_path = initiate_chat_path
        self.discovery_path = discovery_path
        self.ws_path = ws_path

    def _send_initiate_chat_msg(
        self,
        workflow_name: str,
        workflow_uuid: str,
        user_id: Optional[str],
        params: dict[str, Any],
    ) -> InitiateWorkflowModel:
        msg = InititateChatModel(
            workflow_name=workflow_name,
            workflow_uuid=workflow_uuid,
            user_id=user_id,
            params=params,
        )

        payload = msg.model_dump()

        resp = requests.post(
            f"{self.fastapi_url}{self.initiate_chat_path}", json=payload, timeout=5
        )
        retval = InitiateWorkflowModel(**resp.json())
        return retval

    async def _publish_websocket_message(
        self,
        websocket: websockets.WebSocketClientProtocol,
        message: InputResponseModel,
    ) -> None:
        payload = message.model_dump_json()
        await websocket.send(payload)
        logger.info(f"Message sent to websocket ({websocket}): {message}")

    async def _run_websocket_subscriber(
        self,
        ui: UI,
        workflow_name: str,
        workflow_uuid: str,
        user_id: Optional[str],
        from_server_subject: str,
        to_server_subject: str,
        params: dict[str, Any],
    ) -> None:
        # connect_url = self.nats_url
        connect_url = f"{self.fastapi_url}{self.ws_path}"
        async with websockets.connect(connect_url) as websocket:
            init_workflow_msg = InitiateWorkflowModel(
                name=workflow_name,
                workflow_uuid=workflow_uuid,
                user_id=user_id,
                params=params,
            )
            await websocket.send(init_workflow_msg.model_dump_json())

            # message = f"SUB {from_server_subject} 1\r\n"
            # await websocket.send(message)
            # logger.info(f"Subscribed to topic {from_server_subject}")

            while True:
                response = await websocket.recv()
                response = (
                    response.decode() if isinstance(response, bytes) else response
                )

                logger.info(f"Received message: {response}")

                msg = IOMessage.create(**json.loads(response))

                retval = await asyncify(ui.process_message)(msg)
                logger.info(f"Message {msg}: processed with response {retval}")

                if isinstance(msg, AskingMessage):
                    if retval is None:
                        logger.warning(
                            f"Message {msg}: response is None. Skipping response to websocket"
                        )
                    else:
                        await websocket.send(retval)
                        logger.info(
                            f"Message {msg}: response {retval} sent to websocket"
                        )

    def run(
        self,
        name: str,
        ui: UI,
        workflow_uuid: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        workflow_uuid = workflow_uuid or uuid4().hex

        initiate_workflow = self._send_initiate_chat_msg(
            name, workflow_uuid=workflow_uuid, user_id=user_id, params=kwargs
        )
        user_id = initiate_workflow.user_id.hex
        workflow_uuid = initiate_workflow.workflow_uuid.hex

        _from_server_subject = f"chat.client.messages.{user_id}.{workflow_uuid}"
        _to_server_subject = f"chat.server.messages.{user_id}.{workflow_uuid}"

        async def _setup_and_run() -> None:
            await self._run_websocket_subscriber(
                ui,
                name,
                workflow_uuid,
                user_id,
                _from_server_subject,
                _to_server_subject,
                kwargs,
            )

        async def run_lifespan() -> None:
            if not self.is_broker_running:
                self.is_broker_running = True
                await _setup_and_run()
            else:
                await _setup_and_run()

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(run_lifespan())

        return "FastAPIWorkflows.run() completed"

    def _get_workflow_info(self) -> list[dict[str, str]]:
        resp = requests.get(f"{self.fastapi_url}/{self.discovery_path}", timeout=5)
        return resp.json()  # type: ignore [no-any-return]

    def _get_names(self) -> list[str]:
        return [workflow["name"] for workflow in self._get_workflow_info()]

    def _get_description(self, name: str) -> str:
        return next(
            workflow["description"]
            for workflow in self._get_workflow_info()
            if workflow["name"] == name
        )

    @property
    def names(self) -> list[str]:
        return self._get_names()

    def get_description(self, name: str) -> str:
        return self._get_description(name)
