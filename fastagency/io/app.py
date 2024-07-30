from contextlib import asynccontextmanager
from os import environ
from typing import AsyncGenerator, Optional

from faststream import ContextRepo, FastStream
from faststream.nats import JStream, NatsBroker

from ..db.base import BackendDBProtocol, FrontendDBProtocol
from ..db.prisma import PrismaBackendDB, PrismaFrontendDB

nats_url: Optional[str] = environ.get("NATS_URL", None)  # type: ignore[assignment]
if nats_url is None:
    domain: str = environ.get("DOMAIN")  # type: ignore[assignment]
    nats_url = f"tls://{domain}:4222"

username: str = "faststream"
password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

print(f"{nats_url=}")  # noqa
print("Starting IONats faststream app...")  # noqa


@asynccontextmanager
async def lifespan(context: ContextRepo) -> AsyncGenerator[None, None]:
    prisma_backend_db = PrismaBackendDB()
    prisma_frontend_db = PrismaFrontendDB()

    with (
        BackendDBProtocol.set_default(prisma_backend_db),
        FrontendDBProtocol.set_default(prisma_frontend_db),
    ):
        yield


broker = NatsBroker(nats_url, user=username, password=password)
app = FastStream(broker, lifespan=lifespan)

stream = JStream(
    name="FastAgency",
    subjects=[
        # starts new conversation
        "chat.server.initiate_chat",
        # server requests input from client; chat.client.messages.<user_uuid>.<deployment_uuid>.<chat_uuid>
        "chat.client.messages.*.*.*",
        # server prints message to client; chat.server.messages.<user_uuid>.<deployment_uuid>.<chat_uuid>
        "chat.server.messages.*.*.*",
        # "function.server.call",
        # "function.client.call.*",
        # "code.server.execute",
        # "code.client.execute.*",
    ],
)
