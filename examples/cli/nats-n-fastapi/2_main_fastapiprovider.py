from os import environ

from fastapi import FastAPI

from fastagency.ui.fastapi import FastAPIProvider
from fastagency.ui.nats import NatsProvider

nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]

fastapi_user: str = "fastapi"
fastapi_password: str = environ.get("FASTAPI_PASSWORD")  # type: ignore[assignment]

nats_user: str = "faststream"
nats_password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

wf = NatsProvider.Workflows(
    nats_url=environ.get("NATS_URL", None), user=nats_user, password=nats_password
)

provider = FastAPIProvider(
    wf=wf,
    user=fastapi_user,
    password=fastapi_password,
)

# app = FastAPI(lifespan=provider.lifespan)
app = FastAPI()
app.include_router(provider.router)

# todo (both here and in nats provider)
# - route for initiating a chat - DONE
# - route for listing workflows with their descriptions - DONE

# start the provider with the following command
# uvicorn main_mesop:app --reload
