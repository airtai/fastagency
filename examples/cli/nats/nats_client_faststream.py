import asyncio
import uuid
from os import environ

from faststream import FastStream, Logger
from faststream.nats import NatsBroker
from nats.js import api

from fastagency.base import AskingMessage, IOMessage
from fastagency.logging import get_logger
from fastagency.ui.nats import JETSTREAM, InitiateModel, InputResponseModel

logger = get_logger(__name__)

title = "Nats FastStream Client"

nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]
user: str = "faststream"
password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]
broker = NatsBroker(nats_url, user=user, password=password)

app = FastStream(broker=broker, title=title)

user_id = str(uuid.uuid4())
thread_id = str(uuid.uuid4())

i = 0


@broker.subscriber(
    f"chat.client.messages.{user_id}.{thread_id}",
    stream=JETSTREAM,
    deliver_policy=api.DeliverPolicy("all"),
)
async def consume_msg_from_autogen(msg: dict, logger: Logger) -> None:
    global i
    logger.info(
        f"Received message from topic chat.client.messages.{user_id}.{thread_id}: {msg}"
    )
    iomessage = IOMessage.create(**msg)
    if isinstance(iomessage, AskingMessage) and i == 0:
        response = InputResponseModel(
            msg="Start a new conversation", question_id=iomessage.uuid
        )
        await broker.publish(response, f"chat.server.messages.{user_id}.{thread_id}")
        logger.info(
            f"Sent response to topic chat.server.messages.{user_id}.{thread_id}: {response.model_dump_json()}"
        )
        i = i + 1
    elif i != 0 and isinstance(iomessage, AskingMessage):
        logger.info("i is not 0")
        # response = InputResponseModel(
        #     msg="", question_id=iomessage.uuid
        # )
        # await broker.publish(response, f"chat.server.messages.{user_id}.{thread_id}")


@app.after_startup
async def send_initiate_chat_msg() -> None:
    async def _send_initiate_chat_msg():
        init_message = InitiateModel(
            user_id=user_id,
            conversation_id=thread_id,
            msg="Hello, How are you chatbot?",
        )
        await broker.publish(init_message, "chat.server.initiate_chat")
        logger.info(
            f"Message sent to topic chat.server.initiate_chat: {init_message.model_dump_json()}"
        )

    asyncio.create_task(_send_initiate_chat_msg())  # noqa: RUF006
