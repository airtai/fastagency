import os
from typing import Any

from fastagency.adapters.nats import NatsAdapter
from fastapi import FastAPI

from ..workflow import wf

nats_url = os.environ.get("NATS_URL", "nats://localhost:4222")
user: str = os.environ.get("FASTAGENCY_NATS_USER", "fastagency")
password: str = os.environ.get("FASTAGENCY_NATS_PASSWORD", "fastagency_nats_password")

adapter = NatsAdapter(provider=wf, nats_url=nats_url, user=user, password=password)

app = FastAPI(lifespan=adapter.lifespan)


# this is optional, but we would like to see the list of available workflows
@app.get("/")
def list_workflows() -> dict[str, Any]:
    return {"Workflows": {name: wf.get_description(name) for name in wf.names}}


# start the adapter with the following command
# uvicorn my_fastagency_app.deployment.main_1_nats:app --reload
