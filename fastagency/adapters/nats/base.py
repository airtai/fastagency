## IONats part

import asyncio
import os
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from queue import Queue
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from asyncer import asyncify, syncify
from faststream import FastStream, Logger
from faststream.nats import JStream, NatsBroker, NatsMessage
from nats.js import api
from pydantic import BaseModel

from ...base import (
    UI,
    AskingMessage,
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    ProviderProtocol,
    TextInput,
    TextMessage,
    run_workflow,
)
from ...logging import get_logger

if TYPE_CHECKING:
    from faststream.nats.subscriber.asyncapi import AsyncAPISubscriber


class InputResponseModel(BaseModel):
    msg: str
    question_id: Optional[UUID] = None
    error: bool = False


class InitiateModel(BaseModel):
    user_id: UUID
    conversation_id: UUID
    msg: str


logger = get_logger(__name__)

JETSTREAM = JStream(
    name="FastAgency",
    subjects=[
        # starts new conversation (can land on any worker)
        "chat.server.initiate_chat",
        # server requests input from client; chat.client.messages.<user_uuid>.<chat_uuid>
        # we create this topic dynamically => client process consuming NATS can fix its worker
        "chat.client.messages.*.*",
        # server prints message to client; chat.server.messages.<user_uuid>.<chat_uuid>
        # we create this topic dynamically and subscribe to it => worker is fixed
        "chat.server.messages.*.*",
    ],
)


class NatsAdapter(IOMessageVisitor):
    def __init__(
        self,
        provider: ProviderProtocol,
        *,
        nats_url: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        super_conversation: Optional["NatsAdapter"] = None,
    ) -> None:
        """Provider for NATS.

        Args:
            provider (ProviderProtocol): The provider.
            nats_url (Optional[str], optional): The NATS URL. Defaults to None in which case 'nats://localhost:4222' is used.
            user (Optional[str], optional): The user. Defaults to None.
            password (Optional[str], optional): The password. Defaults to None.
            super_conversation (Optional["NatsProvider"], optional): The super conversation. Defaults to None.
        """
        self.provider = provider
        self.nats_url = nats_url or "nats://localhost:4222"
        self.user = user
        self.password = password
        self.queue: Queue = Queue()  # type: ignore[type-arg]

        self.broker = NatsBroker(self.nats_url, user=user, password=password)
        self.app = FastStream(self.broker)
        self.subscriber: "AsyncAPISubscriber"
        self._input_request_subject: str
        self._input_receive_subject: str

        self.super_conversation: Optional[NatsAdapter] = super_conversation
        self.sub_conversations: list[NatsAdapter] = []

        self._create_initiate_subscriber()

    async def _handle_input(
        self, body: InputResponseModel, msg: NatsMessage, logger: Logger
    ) -> None:
        """Handle input from the client by consuming messages from chat.server.messages.*.*.

        Args:
            body (InputResponseModel): The body of the message.
            msg (NatsMessage): The message object.
            logger (Logger): The logger object (gets injected)
        """
        logger.info(
            f"Received message in subject '{self._input_receive_subject}': {body}"
        )
        await msg.ack()
        self.queue.put(msg)

    async def _send_error_msg(self, e: Exception, logger: Logger) -> None:
        """Send an error message.

        Args:
            e (Exception): The exception.
            logger (Logger): The logger object (gets injected)
        """
        logger.error(f"Error in chat: {e}")
        logger.error(traceback.format_exc())

        error_msg = InputResponseModel(msg=str(e), error=True, question_id=None)
        await self.broker.publish(error_msg, self._input_request_subject)

    def _create_initiate_subscriber(self) -> None:
        @self.broker.subscriber(
            "chat.server.initiate_chat",
            stream=JETSTREAM,
            queue="initiate_workers",
            deliver_policy=api.DeliverPolicy("all"),
        )
        async def initiate_handler(
            body: InitiateModel, msg: NatsMessage, logger: Logger
        ) -> None:
            """Initiate the handler.

            1. Subscribes to the chat.server.initiate_chat topic.
            2. When a message is consumed from the topic, it dynamically subscribes to the chat.server.messages.<user_uuid>.<chat_uuid> topic.
            3. Starts the chat workflow after successfully subscribing to the chat.server.messages.<user_uuid>.<chat_uuid> topic.

            Args:
                body (InitiateModel): The body of the message.
                msg (NatsMessage): The message object.
                logger (Logger): The logger object (gets injected)

            """
            await msg.ack()

            logger.info(
                f"Message in subject 'chat.server.initiate_chat': {body=} -> from process id {os.getpid()}"
            )
            user_id = str(body.user_id)
            thread_id = str(body.conversation_id)
            self._input_request_subject = f"chat.client.messages.{user_id}.{thread_id}"
            self._input_receive_subject = f"chat.server.messages.{user_id}.{thread_id}"

            # dynamically subscribe to the chat server
            subscriber = self.broker.subscriber(
                subject=self._input_receive_subject,
                stream=JETSTREAM,
                deliver_policy=api.DeliverPolicy("all"),
            )
            subscriber(self._handle_input)
            self.broker.setup_subscriber(subscriber)
            await subscriber.start()

            try:

                async def start_chat() -> None:  # type: ignore [return]
                    try:
                        await asyncify(run_workflow)(
                            provider=self.provider,
                            ui=self,  # type: ignore[arg-type]
                            name=self.provider.names[0],
                            single_run=True,
                        )

                    except Exception as e:
                        await self._send_error_msg(e, logger)

                background_tasks = set()
                task = asyncio.create_task(start_chat())  # type: ignore
                background_tasks.add(task)

                def callback(t: asyncio.Task[Any]) -> None:
                    try:
                        background_tasks.discard(t)
                        syncify(subscriber.close)()
                    except Exception as e:
                        logger.error(f"Error in callback: {e}")
                        logger.error(traceback.format_exc())

                task.add_done_callback(callback)

            except Exception as e:
                await self._send_error_msg(e, logger)

    # todo: make it a router
    @asynccontextmanager
    async def lifespan(self, app: Any) -> AsyncIterator[None]:
        async with self.broker:
            await self.broker.start()
            try:
                yield
            finally:
                await self.broker.close()

    def visit_default(self, message: IOMessage) -> None:
        content = message.model_dump()
        logger.debug(f"visit_default(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

    def visit_text_message(self, message: TextMessage) -> None:
        content = message.model_dump()
        logger.debug(f"visit_text_message(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

    async def _wait_for_question_response_with_timeout(
        self, question_id: str, *, timeout: int = 180
    ) -> InputResponseModel:
        """Wait for the question response.

        Args:
            question_id (str): The question ID.
            timeout (int, optional): The timeout in seconds. Defaults to 180.
        """
        try:
            # Set a timeout of 180 seconds
            return await asyncio.wait_for(
                self._wait_for_question_response(question_id), timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.debug(
                f"Timeout: User did not send a reply within {timeout} seconds."
            )
            return InputResponseModel(
                msg="User didn't send a reply. Exit the workflow execution.",
                question_id=question_id,
                error=True,
            )

    # todo: we need to add timeout and handle it somehow
    async def _wait_for_question_response(self, question_id: str) -> InputResponseModel:
        while True:
            while self.queue.empty():  # noqa: ASYNC110
                await asyncio.sleep(0.1)

            msg: NatsMessage = self.queue.get()
            input_response = InputResponseModel.model_validate_json(
                msg.raw_message.data.decode("utf-8")
            )

            question_id_hex = (
                input_response.question_id.hex if input_response.question_id else "None"
            )
            logger.debug(question_id_hex)
            logger.debug(question_id)
            logger.debug(question_id_hex == question_id)
            if question_id_hex == question_id:
                logger.debug("Breaking the while loop")
                break
            else:
                self.queue.put(msg)

        logger.debug("Got the response")
        self.queue.task_done()
        return input_response

    def visit_text_input(self, message: TextInput) -> str:
        content = message.model_dump()
        question_id = message.uuid
        logger.info(f"visit_text_input(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

        input_response: InputResponseModel = syncify(
            self._wait_for_question_response_with_timeout
        )(question_id=question_id)
        logger.info(input_response)
        return input_response.msg

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        content = message.model_dump()
        question_id = message.uuid
        logger.info(f"visit_multiple_choice(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

        input_response: InputResponseModel = syncify(
            self._wait_for_question_response_with_timeout
        )(question_id=question_id)
        logger.info(input_response)
        return input_response.msg

    def process_message(self, message: IOMessage) -> Optional[str]:
        try:
            return self.visit(message)
        except Exception as e:
            logger.error(f"Error in process_message: {e}", stack_info=True)
            # do not reraise, we must go on
            if isinstance(message, AskingMessage):
                return "Error: Something went wrong. Please check logs for details."
            return None

    def create_subconversation(self) -> "NatsAdapter":
        return self

    @classmethod
    def create_provider(
        cls,
        nats_url: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> ProviderProtocol:
        return NatsProvider(nats_url=nats_url, user=user, password=password)


class NatsProvider:
    def __init__(
        self,
        nats_url: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """Initialize the nats workflows.

        Args:
            nats_url (Optional[str], optional): The NATS URL. Defaults to None.
            user (Optional[str], optional): The user. Defaults to None.
            password (Optional[str], optional): The password. Defaults to None.
        """
        # self._workflows: dict[
        #     str, tuple[Callable[[WorkflowsProtocol, UI, str, str], str], str]
        # ] = {}

        self.nats_url = nats_url or "nats://localhost:4222"
        self.user = user
        self.password = password

        self.broker = NatsBroker(self.nats_url, user=self.user, password=self.password)
        self.app = FastStream(self.broker)

        self._initiate_chat_subject: str = "chat.server.initiate_chat"

        self.is_broker_running: bool = False

    async def _setup_subscriber(
        self, ui: UI, from_server_subject: str, to_server_subject: str
    ) -> None:
        logger.info(
            f"Setting up subscriber for {from_server_subject=}, {to_server_subject=}"
        )

        async def consume_msg_from_nats(msg: dict[str, Any], logger: Logger) -> None:
            logger.debug(f"Received message from topic {from_server_subject}: {msg}")
            iomessage = (
                IOMessage.create(**{"type": "error", "long": msg["msg"]})
                if msg.get("error")
                else IOMessage.create(**msg)
            )
            if isinstance(iomessage, AskingMessage):
                processed_message = ui.process_message(iomessage)
                response = InputResponseModel(
                    msg=processed_message, question_id=iomessage.uuid
                )
                logger.debug(f"Processed response: {response}")
                await self.broker.publish(response, to_server_subject)
            else:
                ui.process_message(iomessage)

        subscriber = self.broker.subscriber(
            from_server_subject,
            stream=JETSTREAM,
            deliver_policy=api.DeliverPolicy("all"),
        )
        subscriber(consume_msg_from_nats)
        self.broker.setup_subscriber(subscriber)
        await subscriber.start()
        logger.info(f"Subscriber for {from_server_subject} started")

    def run(self, name: str, session_id: Optional[UUID] = None, ui: UI) -> str:
        # subscribe to whatever topic you need
        # consume a message from the topic and call that visitor pattern (which is happening in NatsProvider)
        user_id = uuid4()  # todo: fix me later
        conversation_id = uuid4()
        init_message = InitiateModel(
            user_id=user_id,
            conversation_id=conversation_id,
        )
        _from_server_subject = f"chat.client.messages.{user_id}.{conversation_id}"
        _to_server_subject = f"chat.server.messages.{user_id}.{conversation_id}"

        async def send_initiate_chat_msg() -> None:
            await self.broker.publish(init_message, self._initiate_chat_subject)
            logger.info("Initiate chat message sent")

        @asynccontextmanager
        async def lifespan() -> AsyncIterator[None]:
            async with self.broker:
                await self.broker.start()
                logger.debug("Broker started")
                try:
                    yield
                finally:
                    await self.broker.close()

        async def _setup_and_run() -> None:
            await send_initiate_chat_msg()
            await self._setup_subscriber(ui, _from_server_subject, _to_server_subject)
            while True:  # noqa: ASYNC110
                await asyncio.sleep(0.1)

        async def run_lifespan() -> None:
            if not self.is_broker_running:
                self.is_broker_running = True
                async with lifespan():
                    await _setup_and_run()
            else:
                await _setup_and_run()

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(run_lifespan())

        return "NatsWorkflows.run() completed"

    @property
    def names(self) -> list[str]:
        return ["simple_learning"]

    def get_description(self, name: str) -> str:
        return "Student and teacher learning chat"
