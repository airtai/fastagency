from os import environ
from typing import Optional

from faststream import FastStream
from faststream.nats import JStream, NatsBroker

nats_url: Optional[str] = environ.get("NATS_URL", None)  # type: ignore[assignment]

if nats_url is None:
    domain: str = environ.get("DOMAIN")  # type: ignore[assignment]
    username: str = "faststream"
    password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]
    nats_url = f"tls://{username}:{password}@{domain}:4222"

print(f"{nats_url=}")  # noqa
print("Starting IONats faststream app...")  # noqa

broker = NatsBroker(nats_url)
app = FastStream(broker)

stream = JStream(
    name="FastAgency",
    subjects=[
        # starts new conversation
        "chat.server.initiate_chat",
        # server requests input from client
        "chat.client.messages.*",
        # server prints message to client
        "chat.server.messages.*",
        # "function.server.call",
        # "function.client.call.*",
        # "code.server.execute",
        # "code.client.execute.*",
    ],
)
