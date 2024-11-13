from os import environ

from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.adapters.nats import NatsAdapter
from fastapi import FastAPI

nats_url = environ.get("NATS_URL", "nats://localhost:4222")
nats_user: str = "fastagency"
nats_password: str = environ.get("FASTAGENCY_NATS_PASSWORD", "fastagency_nats_password")

provider = NatsAdapter.create_provider(
    nats_url=nats_url, user=nats_user, password=nats_password
)

adapter = FastAPIAdapter(
    provider=provider,
)

app = FastAPI()
app.include_router(adapter.router)


# this is optional, but we would like to see the list of available workflows
@app.get("/")
def read_root() -> dict[str, dict[str, str]]:
    return {
        "Workflows": {name: provider.get_description(name) for name in provider.names}
    }


# start the provider with the following command
# uvicorn my_fastagency_app.deployment.main_2_fastapi:app --host 0.0.0.0 --port 8008 --reload
