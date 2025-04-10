## IONats part

import asyncio
import os
import traceback
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from queue import Queue
from typing import TYPE_CHECKING, Any, Optional

from asyncer import asyncify, syncify
from faststream import FastStream, Logger
from faststream.nats import JStream, NatsBroker, NatsMessage
from nats.aio.client import Client as NatsClient
from nats.errors import NoServersError
from nats.js import JetStreamContext, api
from nats.js.errors import KeyNotFoundError, NoKeysError
from nats.js.kv import KeyValue

from ...base import UI, CreateWorkflowUIMixin, ProviderProtocol, Runnable, UIBase
from ...exceptions import FastAgencyNATSConnectionError, FastAgencyNATSKeyError
from ...logging import get_logger
from ...messages import (
    AskingMessage,
    IOMessage,
    InitiateWorkflowModel,
    InputResponseModel,
    MessageProcessorMixin,
    MultipleChoice,
    TextInput,
    TextMessage,
)

if TYPE_CHECKING:
    from faststream.nats.subscriber.asyncapi import AsyncAPISubscriber


logger = get_logger(__name__)

JETSTREAM = JStream(
    name="FastAgency",
    subjects=[
        # starts new conversation (can land on any worker)
        "chat.server.initiate_chat",
        # server requests input from client; chat.client.messages.<user_uuid>.<workflow_uuid>
        # we create this topic dynamically => client process consuming NATS can fix its worker
        "chat.client.messages.*.*",
        # server prints message to client; chat.server.messages.<user_uuid>.<workflow_uuid>
        # we create this topic dynamically and subscribe to it => worker is fixed
        "chat.server.messages.*.*",
        # discovery subject
        "discovery",
    ],
)


class NatsAdapter(MessageProcessorMixin, CreateWorkflowUIMixin):
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

        error_msg = InputResponseModel(msg=str(e), error=True, question_uuid=None)
        await self.broker.publish(error_msg, self._input_request_subject)

    def _create_initiate_subscriber(self) -> None:
        @self.broker.subscriber(
            "chat.server.initiate_chat",
            stream=JETSTREAM,
            queue="initiate_workers",
            deliver_policy=api.DeliverPolicy("all"),
        )
        async def initiate_handler(
            body: InitiateWorkflowModel, msg: NatsMessage, logger: Logger
        ) -> None:
            """Initiate the handler.

            1. Subscribes to the chat.server.initiate_chat topic.
            2. When a message is consumed from the topic, it dynamically subscribes to the chat.server.messages.<user_uuid>.<workflow_uuid> topic.
            3. Starts the chat workflow after successfully subscribing to the chat.server.messages.<user_uuid>.<workflow_uuid> topic.

            Args:
                body (InitiateModel): The body of the message.
                msg (NatsMessage): The message object.
                logger (Logger): The logger object (gets injected)

            """
            await msg.ack()

            logger.info(
                f"Message in subject 'chat.server.initiate_chat': {body=} -> from process id {os.getpid()}"
            )
            user_id = body.user_id if body.user_id else "None"
            workflow_uuid = body.workflow_uuid.hex
            self._input_request_subject = (
                f"chat.client.messages.{user_id}.{workflow_uuid}"
            )
            self._input_receive_subject = (
                f"chat.server.messages.{user_id}.{workflow_uuid}"
            )

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

                async def start_chat(
                    ui_base: UIBase,
                    provider: ProviderProtocol,
                    name: str,
                    params: dict[str, Any],
                    workflow_uuid: str,
                ) -> None:  # type: ignore [return]
                    def _start_chat(
                        ui_base: UIBase,
                        provider: ProviderProtocol,
                        name: str,
                        params: dict[str, Any],
                        workflow_uuid: str,
                    ) -> None:  # type: ignore [return]
                        ui: UI = ui_base.create_workflow_ui(workflow_uuid=workflow_uuid)
                        try:
                            provider.run(
                                name=name,
                                ui=ui,
                                **params,
                            )
                        except Exception as e:
                            logger.error(
                                f"Unexpecter error in NatsAdapter.start_chat: {e}",
                                stack_info=True,
                            )
                            ui.error(
                                sender="NatsAdapter",
                                short=f"Unexpected error: {e}",
                                long=traceback.format_exc(),
                            )
                            return

                    return await asyncify(_start_chat)(
                        ui_base, provider, name, params, workflow_uuid
                    )

                background_tasks = set()
                task = asyncio.create_task(
                    start_chat(
                        self, self.provider, body.name, body.params, workflow_uuid
                    )
                )  # type: ignore
                background_tasks.add(task)

                async def callback(t: asyncio.Task[Any]) -> None:
                    try:
                        background_tasks.discard(t)
                        await subscriber.close()
                    except Exception as e:
                        logger.error(f"Error in callback: {e}")
                        logger.error(traceback.format_exc())

                task.add_done_callback(lambda t: asyncio.create_task(callback(t)))

            except Exception as e:
                await self._send_error_msg(e, logger)

    async def _publish_discovery(self) -> None:
        """Publish the discovery message."""
        jetstream_key_value = await self.broker.key_value(bucket="discovery")

        names = self.provider.names
        for name in names:
            description = self.provider.get_description(name)
            await jetstream_key_value.put(name, description.encode())

    # todo: make it a router
    @asynccontextmanager
    async def lifespan(self, app: Any) -> AsyncIterator[None]:
        async with self.broker:
            await self.broker.start()
            await self._publish_discovery()
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
                question_uuid=question_id,
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
                input_response.question_uuid.hex
                if input_response.question_uuid
                else "None"
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
        logger.info(
            f"visit_text_input(): published message '{content}' to {self._input_request_subject}"
        )

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

    @contextmanager
    def create(self, app: Runnable, import_string: str) -> Iterator[None]:
        raise NotImplementedError("NatsAdapter.create() is not implemented")

    def start(
        self,
        *,
        app: Runnable,
        import_string: str,
        name: Optional[str] = None,
        params: dict[str, Any],
        single_run: bool = False,
    ) -> None:
        raise NotImplementedError("NatsAdapter.start() is not implemented")


class NatsProvider(ProviderProtocol):
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
                    msg=processed_message, question_uuid=iomessage.uuid
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

    def run(
        self,
        name: str,
        ui: UI,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        # subscribe to whatever topic you need
        # consume a message from the topic and call that visitor pattern (which is happening in NatsProvider)
        workflow_uuid = ui._workflow_uuid
        init_message = InitiateWorkflowModel(
            user_id=user_id,
            workflow_uuid=workflow_uuid,
            params=kwargs,
            name=name,
        )
        _from_server_subject = f"chat.client.messages.{user_id}.{workflow_uuid}"
        _to_server_subject = f"chat.server.messages.{user_id}.{workflow_uuid}"

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

    @asynccontextmanager
    async def _get_jetstream_context(self) -> AsyncIterator[JetStreamContext]:
        nc = NatsClient()
        await nc.connect(self.nats_url, user=self.user, password=self.password)
        js = nc.jetstream()
        try:
            yield js
        finally:
            await nc.close()

    @asynccontextmanager
    async def _get_jetstream_key_value(
        self, bucket: str = "discovery"
    ) -> AsyncIterator[KeyValue]:
        async with self._get_jetstream_context() as js:
            kv = await js.create_key_value(bucket=bucket)
            yield kv

    async def _get_names(self) -> list[str]:
        try:
            async with self._get_jetstream_key_value() as kv:
                names = await kv.keys()
        except NoKeysError:
            names = []
        except NoServersError as e:
            raise FastAgencyNATSConnectionError(
                f"Unable to connect to NATS server at {self.nats_url}"
            ) from e

        return names

    async def _get_description(self, name: str) -> str:
        try:
            async with self._get_jetstream_key_value() as kv:
                description = await kv.get(name)
            return description.value.decode() if description.value else ""
        except KeyNotFoundError as e:
            raise FastAgencyNATSKeyError(
                f"Workflow name {name} not found to get description"
            ) from e
        except NoServersError as e:
            raise FastAgencyNATSConnectionError(
                f"Unable to connect to NATS server at {self.nats_url}"
            ) from e

    @property
    def names(self) -> list[str]:
        names = asyncio.run(self._get_names())
        logger.debug(f"Names: {names}")
        # return ["simple_learning"]
        return names

    def get_description(self, name: str) -> str:
        description = asyncio.run(self._get_description(name))
        logger.debug(f"Description: {description}")
        # return "Student and teacher learning chat"
        return description
