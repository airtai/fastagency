from fastapi import FastAPI

from fastagency.adapters.fastapi import FastAPIAdapter

from .workflow import wf


adapter = FastAPIAdapter(provider=wf)

app = FastAPI()
app.include_router(adapter.router)


# this is optional, but we would like to see the list of available workflows
@app.get("/")
def read_root() -> dict[str, dict[str, str]]:
    return {"Workflows": {name: wf.get_description(name) for name in wf.names}}


# start the provider with the following command
# uvicorn main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
