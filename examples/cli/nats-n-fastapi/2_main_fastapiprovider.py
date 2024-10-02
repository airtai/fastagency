from os import environ

from fastapi import FastAPI

from fastagency.ui.fastapi import FastAPIProvider
from fastagency.ui.nats import NatsProvider

nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]

fastapi_user: str = "fastapi"
fastapi_password: str = environ.get("FASTAPI_PASSWORD")  # type: ignore[assignment]

nats_user: str = "faststream"
nats_password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

wf = NatsProvider.Workflows(nats_url=environ.get("NATS_URL", None), user=nats_user, password=nats_password)

provider = FastAPIProvider(wf=wf, fastapi_url=environ.get("FASTAPI_URL", None), user=fastapi_user, password=fastapi_password)

app = FastAPI(lifespans=provider.lifespan)

# todo (both here and in nats provider)
# - route for initiating a chat
# - route for listing workflows with their descriptions

# start the provider with the following command
# uvicorn main_mesop:app --reload
