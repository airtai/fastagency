## IONats part

import asyncio
import os
import traceback
from collections.abc import AsyncIterator, Iterable, Mapping
from contextlib import asynccontextmanager
from queue import Queue
from typing import TYPE_CHECKING, Any, Callable, Optional, Union
from uuid import UUID, uuid4

from asyncer import asyncify, syncify
from faststream import FastStream, Logger
from faststream.nats import JStream, NatsBroker, NatsMessage
from nats.js import api
from pydantic import BaseModel

from fastagency.logging import get_logger

from ...base import (
    Agent,
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    TextInput,
    TextMessage,
    Workflow,
    Workflows,
    run_workflow,
)

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


class NatsProvider(IOMessageVisitor):
    def __init__(
        self,
        wf: Workflows,
        *,
        nats_url: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        super_conversation: Optional["NatsProvider"] = None,
    ) -> None:
        """Provider for NATS.

        Args:
            wf (Workflows): The workflow object.
            nats_url (Optional[str], optional): The NATS URL. Defaults to None in which case 'nats://localhost:4222' is used.
            user (Optional[str], optional): The user. Defaults to None.
            password (Optional[str], optional): The password. Defaults to None.
            super_conversation (Optional["NatsProvider"], optional): The super conversation. Defaults to None.
        """
        self.wf = wf
        self.nats_url = nats_url or "nats://localhost:4222"
        self.user = user
        self.password = password
        self.queue: Queue = Queue()  # type: ignore[type-arg]

        self.broker = NatsBroker(self.nats_url, user=user, password=password)
        self.app = FastStream(self.broker)
        self.subscriber: "AsyncAPISubscriber"
        self._input_request_subject: str
        self._input_receive_subject: str

        self.super_conversation: Optional[NatsProvider] = super_conversation
        self.sub_conversations: list[NatsProvider] = []

        self.stream = JStream(
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

        self.create_initiate_subscriber()

    async def handle_input(
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

        self.queue.put(msg)

    async def send_error_msg(self, e: Exception, logger: Logger) -> None:
        """Send an error message.

        Args:
            e (Exception): The exception.
            logger (Logger): The logger object (gets injected)
        """
        logger.error(f"Error in chat: {e}")
        logger.error(traceback.format_exc())

        error_msg = InputResponseModel(msg=str(e), error=True, question_id=None)
        await self.broker.publish(error_msg, self._input_request_subject)

    # @broker.subscriber(
    #     "chat.server.initiate_chat",
    #     stream=stream,
    #     queue="initiate_workers",
    #     deliver_policy=api.DeliverPolicy("all"),
    # )
    def create_initiate_subscriber(self):
        @self.broker.subscriber(
            "chat.server.initiate_chat",
            stream=self.stream,
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
                stream=self.stream,
                deliver_policy=api.DeliverPolicy("all"),
            )
            subscriber(self.handle_input)
            self.broker.setup_subscriber(subscriber)
            await subscriber.start()

            try:

                async def start_chat() -> None:  # type: ignore [return]
                    try:
                        logger.info("Above self.wf.run")
                        await asyncify(run_workflow)(
                            wf=self.wf,
                            ui=self,  # type: ignore[arg-type]
                            name=self.wf.names[0],
                            initial_message=body.msg,
                            single_run=False,
                        )

                    except Exception as e:
                        await self.send_error_msg(e, logger)

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
                await self.send_error_msg(e, logger)

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

    # todo: we need to add timeout and handle it somehow
    async def wait_for_question_response(self, question_id: str) -> InputResponseModel:
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
        await msg.ack()
        return input_response

    def visit_text_input(self, message: TextInput) -> str:
        content = message.model_dump()
        question_id = message.uuid
        logger.info(f"visit_text_input(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

        input_response: InputResponseModel = syncify(self.wait_for_question_response)(
            question_id=question_id
        )
        logger.info(input_response)
        return input_response.msg

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        content = message.model_dump()
        question_id = message.uuid
        logger.info(f"visit_multiple_choice(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

        input_response: InputResponseModel = syncify(self.wait_for_question_response)(
            question_id=question_id
        )
        logger.info(input_response)
        return input_response.msg

    def visit(self, message: IOMessage) -> Optional[str]:
        method_name = f"visit_{message.type}"
        method = getattr(self, method_name, self.visit_default)
        return method(message)

    def process_message(self, message: IOMessage) -> Optional[str]:
        # logger.info(f"process_message(): {message=}")
        try:
            return self.visit(message)
        except Exception as e:
            logger.error(f"Error in process_message: {e}", stack_info=True)
            raise

    def create_subconversation(self) -> "NatsProvider":
        return self

    @property
    def Workflows(self) -> Workflows:  # noqa: N802
        return NatsWorkflows


class NatsWorkflows(Workflows):
    def register(self, name: str, description: str) -> Callable[[Workflow], Workflow]:
        raise NotImplementedError("Just ignore this for now")

    def run(self, name: str, session_id: str, ui: UI, initial_message: str) -> str:
        # subscribe to whatever topic you need
        # consume a message from the topic and call that visitor pattern (which is happening in NatsProvider)
        user_id = uuid4()  # todo: fix me later
        conversation_id = uuid4()
        raise NotImplementedError("Implement me")

    @property
    def names(self) -> list[str]:
        raise NotImplementedError(
            "Just ignore this for now, should be implemented later"
        )

    def get_description(self, name: str) -> str:
        raise NotImplementedError(
            "Just ignore this for now, should be implemented later"
        )

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
            "Just ignore this for now, will be removed from this protocol"
        )
