import json
import random
from os import environ
from typing import Any, Optional

from faststream import FastStream, Logger
from faststream.nats import JStream, NatsBroker, NatsMessage

process_id = random.randint(1, 1000)  # nosec B311

nats_url: Optional[str] = environ.get("NATS_URL", None)  # type: ignore[assignment]
if nats_url is None:
    domain: str = environ.get("DOMAIN")  # type: ignore[assignment]
    nats_url = f"tls://{domain}:4222"

username: str = "faststream"
password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

print(f"{nats_url=}")  # noqa
print("Starting PING PONG faststream app...")  # noqa

broker = NatsBroker(nats_url, user=username, password=password)
app = FastStream(broker)

stream = JStream(name="ping_pong", subjects=["ping.*", "pong.*"])


async def ping_handler(body: dict[str, Any], msg: NatsMessage, logger: Logger) -> None:
    raw_message = msg.raw_message

    subject = raw_message.subject
    client_id = subject.split(".")[1]
    reply_subject = raw_message.reply

    await msg.ack()
    logger.info(
        f"Received a message on '{subject=} {reply_subject=}': {body=} -> from {process_id=}"
    )

    if "msg" not in body or body["msg"].lower() != "ping":
        reply_msg = f"Unkown message: {body}, please send 'ping' in body['msg']"
    else:
        reply_msg = "pong"

    reply = {
        "msg": reply_msg,
        "process_id": process_id,
    }
    await broker.publish(json.dumps(reply), f"pong.{client_id}")


@broker.subscriber(
    "register.*",
    stream=stream,
    queue="register_workers",
)
async def register_handler(
    body: dict[str, Any], msg: NatsMessage, logger: Logger
) -> None:
    raw_message = msg.raw_message

    subject = raw_message.subject
    client_id = subject.split(".")[1]
    reply = raw_message.reply

    await msg.ack()

    logger.info(
        f"Received a message on '{subject=} {reply=}': {body=} -> from {process_id=}"
    )

    logger.info(f"Creating a new subscriber for {client_id=}")

    subscriber = broker.subscriber(
        f"ping.{client_id}",
        stream=stream,
    )
    subscriber(ping_handler)

    broker.setup_subscriber(subscriber)
    # print(broker)
    # print(type(broker))
    # print(dir(broker))
    await subscriber.start()
