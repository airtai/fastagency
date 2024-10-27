import os

from fastapi import FastAPI

from workflow import wf as chess_wf

from fastagency.adapters.fastapi import FastAPIAdapter

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

adapter = FastAPIAdapter(provider=chess_wf)

app = FastAPI()
app.include_router(adapter.router)


# this is optional, but we would like to see the list of available workflows
@app.get("/")
def read_root() -> dict[str, dict[str, str]]:
    return {
        "Workflows": {name: chess_wf.get_description(name) for name in chess_wf.names}
    }


# start the provider with the following command
# uvicorn main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
