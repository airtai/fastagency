import os
from typing import Any

from fastapi import FastAPI
from fastagency.adapters.fastapi import FastAPIAdapter

from ..workflow import wf


adapter = FastAPIAdapter(provider=wf)

app = FastAPI()
app.include_router(adapter.router)


# this is optional, but we would like to see the list of available workflows
@app.get("/")
def list_workflows() -> dict[str, Any]:
    return {"Workflows": {name: wf.get_description(name) for name in wf.names}}


# start the adapter with the following command
# uvicorn my_fastagency_app.deployment.main_1_fastapi:app --reload
