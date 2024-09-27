## IONats part

import asyncio
import os
import time
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from queue import Queue
from typing import TYPE_CHECKING, Any, Literal, Optional, Union
from uuid import UUID

from asyncer import asyncify, syncify
from faststream import FastStream, Logger
from faststream.nats import JStream, NatsBroker, NatsMessage
from nats.js import api
from pydantic import BaseModel

from fastagency.logging import get_logger

from ...base import (
    IOMessage,
    IOMessageVisitor,
    MultipleChoice,
    TextInput,
    TextMessage,
    Workflows,
    run_workflow,
)

if TYPE_CHECKING:
    from faststream.nats.subscriber.asyncapi import AsyncAPISubscriber


class PrintModel(BaseModel):
    msg: str


class InputRequestModel(BaseModel):
    prompt: str
    is_password: bool


class InputResponseModel(BaseModel):
    msg: str
    question_id: UUID


class TerminateModel(BaseModel):
    msg: str = "Chat completed."


class ErrorResoponseModel(BaseModel):
    msg: str


TYPE_LITERAL = Literal["input", "print", "terminate", "error"]


class ServerResponseModel(BaseModel):
    data: Union[InputRequestModel, PrintModel, TerminateModel, ErrorResoponseModel]
    type: TYPE_LITERAL


class InitiateModel(BaseModel):
    user_id: UUID
    thread_id: UUID
    msg: str


logger = get_logger(__name__)


class UpdatedNatsProvider(IOMessageVisitor):
    def __init__(
        self,
        wf: Workflows,
        nats_url: str,
        user: str,
        password: str,
        super_conversation: Optional["UpdatedNatsProvider"] = None,
    ) -> None:
        """Provider for NATS."""
        self.wf = wf
        self.nats_url = nats_url
        self.user = user
        self.password = password
        self.queue: Queue = Queue()  # type: ignore[type-arg]

        self.broker = NatsBroker(nats_url, user=user, password=password)
        self.app = FastStream(self.broker)
        self._publisher = self.broker.publish
        self.subscriber: "AsyncAPISubscriber"
        self._input_request_subject: str
        self._input_receive_subject: str

        self.super_conversation: Optional[UpdatedNatsProvider] = super_conversation
        self.sub_conversations: list[UpdatedNatsProvider] = []

        self.stream = JStream(
            name="FastAgency",
            subjects=[
                # starts new conversation
                "chat.server.initiate_chat",
                # server requests input from client; chat.client.messages.<user_uuid>.<chat_uuid>
                "chat.client.messages.*.*",
                # server prints message to client; chat.server.messages.<user_uuid>.<chat_uuid>
                "chat.server.messages.*.*",
            ],
        )

    async def handle_input(
        self, body: InputResponseModel, msg: NatsMessage, logger: Logger
    ) -> None:
        logger.info(
            f"Received message in subject '{self._input_receive_subject}': {body}"
        )

        self.queue.put(msg)

    # @broker.subscriber(
    #     "chat.server.initiate_chat",
    #     stream=stream,
    #     queue="initiate_workers",
    #     deliver_policy=api.DeliverPolicy("all"),
    # )
    async def initiate_handler(
        self, body: InitiateModel, msg: NatsMessage, logger: Logger
    ) -> None:
        await msg.ack()

        logger.info(
            f"Message in subject 'chat.server.initiate_chat': {body=} -> from process id {os.getpid()}"
        )
        user_id = str(body.user_id)
        thread_id = str(body.thread_id)
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

            def start_chat() -> None:  # type: ignore [return]
                try:
                    terminate_data = TerminateModel()
                    terminate_chat_msg = ServerResponseModel(
                        data=terminate_data, type="terminate"
                    )
                    logger.info("Above self.wf.run")
                    # chat_result = self.wf.run(
                    #     name = self.wf.names[0],
                    #     session_id="session_id",
                    #     ui=self.ui.create_subconversation(),
                    #     initial_message=body.msg
                    # )
                    run_workflow(
                        wf=self.wf,
                        ui=self,  # type: ignore[arg-type]
                        name=self.wf.names[0],
                        initial_message=body.msg,
                        single_run=False,
                    )

                    syncify(self.broker.publish)(
                        terminate_chat_msg, self._input_request_subject
                    )  # type: ignore [arg-type]
                except Exception as e:
                    logger.error(f"Error in chat: {e}")
                    logger.error(traceback.format_exc())

                    error_data = ErrorResoponseModel(msg=str(e))
                    error_msg = ServerResponseModel(data=error_data, type="error")
                    syncify(self.broker.publish)(error_msg, self._input_request_subject)

            async_start_chat = asyncify(start_chat)

            background_tasks = set()
            task = asyncio.create_task(async_start_chat())  # type: ignore
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
            logger.error(f"Error in handling initiate chat: {e}")
            logger.error(traceback.format_exc())

            error_data = ErrorResoponseModel(msg=str(e))
            error_msg = ServerResponseModel(data=error_data, type="error")
            syncify(self.broker.publish)(error_msg, self._input_request_subject)  # type: ignore [arg-type]

    @asynccontextmanager
    async def start(self, app: Any) -> AsyncIterator[None]:
        async with self.broker:
            await self.broker.start()
            init_chat_subscriber = self.broker.subscriber(
                subject="chat.server.initiate_chat",
                stream=self.stream,
                queue="initiate_workers",
                deliver_policy=api.DeliverPolicy("all"),
            )
            init_chat_subscriber(self.initiate_handler)
            self.broker.setup_subscriber(init_chat_subscriber)
            await init_chat_subscriber.start()
            try:
                yield
            finally:
                await self.broker.close()

    def visit_default(self, message: IOMessage) -> None:
        content = message.model_dump()
        logger.info(f"visit_default(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

    def visit_text_message(self, message: TextMessage) -> None:
        content = message.model_dump()
        logger.info(f"visit_text_message(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

    def wait_for_question_response(self, question_id: str) -> InputResponseModel:
        while True:
            while self.queue.empty():
                time.sleep(0.1)

            msg: NatsMessage = self.queue.get()
            input_response = InputResponseModel.model_validate_json(
                msg.raw_message.data.decode("utf-8")
            )
            logger.info(str(input_response.question_id.hex))
            logger.info(question_id)
            logger.info(str(input_response.question_id.hex) == question_id)
            if str(input_response.question_id.hex) == question_id:
                logger.info("Breaking the while loop")
                break
            else:
                self.queue.put(msg)
        logger.info("Got the response")
        self.queue.task_done()
        syncify(msg.ack)()
        return input_response

    def visit_text_input(self, message: TextInput) -> str:
        content = message.model_dump()
        question_id = message.uuid
        logger.info(f"visit_text_input(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

        input_response: InputResponseModel = self.wait_for_question_response(
            question_id=question_id
        )
        logger.info(input_response)
        return input_response.msg

    def visit_multiple_choice(self, message: MultipleChoice) -> str:
        content = message.model_dump()
        question_id = message.uuid
        logger.info(f"visit_multiple_choice(): {content=}")
        syncify(self.broker.publish)(content, self._input_request_subject)

        # wait for the input to arrive and be propagated to queue
        # while self.queue.empty():
        #     time.sleep(0.1)

        # msg: NatsMessage = self.queue.get()

        # self.queue.task_done()
        # syncify(msg.ack)()
        input_response: InputResponseModel = self.wait_for_question_response(
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
        return self.visit(message)

    def create_subconversation(self) -> "UpdatedNatsProvider":
        # sub_conversation = UpdatedNatsProvider(wf=self.wf, nats_url=self.nats_url, user=self.user, password=self.password, super_conversation=self)
        # sub_conversation._input_receive_subject = self._input_receive_subject
        # sub_conversation._input_request_subject = self._input_request_subject
        # self.sub_conversations.append(sub_conversation)

        # return sub_conversation
        return self
