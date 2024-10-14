import contextlib
import os
import socket
import threading
import time
from collections.abc import Iterator
from platform import system
from typing import (
    Annotated,
    Any,
    Callable,
    Optional,
    TypeVar,
)
from unittest.mock import MagicMock

import fastapi
import openai
import pytest
import uvicorn
from fastapi import FastAPI, Path
from pydantic import BaseModel
from pydantic import __version__ as version_of_pydantic

from .helpers import tag

F = TypeVar("F", bound=Callable[..., Any])


# Modify pytest's default behavior to treat "no tests collected" (exit code 5) as a success (exit code 0),
# useful for CI/CD pipelines to avoid failures when no tests match filters.
# https://docs.pytest.org/en/stable/reference/exit-codes.html
def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    if exitstatus == 5:
        pytest.exit("No tests were collected, treating as success.", 0)


################################################################################
###
# Fixtures for LLMs
###
################################################################################


def azure_model_llm_config(model_env_name: str) -> dict[str, Any]:
    api_key = os.getenv("AZURE_OPENAI_API_KEY", default="*" * 64)
    api_base = os.getenv(
        "AZURE_API_ENDPOINT", default="https://my-deployment.openai.azure.com"
    )

    def get_default_model_name(model_env_name: str) -> str:
        if model_env_name == "AZURE_GPT35_MODEL":
            return "gpt-35-turbo-16k"
        elif model_env_name == "AZURE_GPT4_MODEL":
            return "gpt-4"
        elif model_env_name == "AZURE_GPT4o_MODEL":
            return "gpt-4o"
        else:
            raise ValueError(f"Unknown model_env_name: {model_env_name}")

    default_model_env_name = get_default_model_name(model_env_name)
    gpt_model_name = os.getenv(model_env_name, default=default_model_env_name)

    openai.api_type = "azure"
    openai.api_version = os.getenv("AZURE_API_VERSION", default="2024-02-01")

    config_list = [
        {
            "model": gpt_model_name,
            "api_key": api_key,
            "base_url": api_base,
            "api_type": openai.api_type,
            "api_version": openai.api_version,
        }
    ]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.8,
    }

    return llm_config


@tag("llm_config")
@pytest.fixture
def azure_gpt35_turbo_16k_llm_config() -> dict[str, Any]:
    return azure_model_llm_config("AZURE_GPT35_MODEL")


@tag("llm_config")
@pytest.fixture
def azure_gpt4_llm_config() -> dict[str, Any]:
    return azure_model_llm_config("AZURE_GPT4_MODEL")


@tag("llm_config")
@pytest.fixture
def azure_gpt4o_llm_config() -> dict[str, Any]:
    return azure_model_llm_config("AZURE_GPT4o_MODEL")


def openai_llm_config(model: str) -> dict[str, Any]:
    zeros = "0" * 20
    api_key = os.getenv("OPENAI_API_KEY", default=f"sk-{zeros}T3BlbkFJ{zeros}")

    config_list = [
        {
            "model": model,
            "api_key": api_key,
        }
    ]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.8,
    }

    return llm_config


@tag("llm_config")
@pytest.fixture
def openai_gpt35_turbo_16k_llm_config() -> dict[str, Any]:
    return openai_llm_config("gpt-3.5-turbo")


@tag("llm_config")
@pytest.fixture
def openai_gpt4o_llm_config() -> dict[str, Any]:
    return openai_llm_config("gpt-4o")


@tag("llm_config")
@pytest.fixture
def openai_gpt4o_mini_llm_config() -> dict[str, Any]:
    return openai_llm_config("gpt-4o-mini")


################################################################################
###
# Fixtures for Toolkit
###
################################################################################


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


def create_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ]
    )

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {"Hello": "World"}

    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: Optional[str] = None) -> dict[str, Any]:
        return {"item_id": item_id, "q": q}

    @app.post("/items")
    async def create_item(item: Item) -> Item:
        return item

    return app


def create_weather_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(
        title="Weather",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    @app.get("/forecast/{city}", description="Get the weather forecast for a city")
    def forecast(
        city: Annotated[str, Path(description="name of the city")],
    ) -> str:
        return f"Weather in {city} is sunny"

    return app


def create_gify_fastapi_app(host: str, port: int) -> FastAPI:
    class Gif(BaseModel):
        id: int
        title: str
        url: str

    app = FastAPI(
        title="Gify",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    @app.get("/gifs", response_model=list[Gif], tags=["gifs"])
    # TODO: API is failing if Query alias contains uppercase letters e.g. alias="Topic"
    def get_gifs_for_topic(topic: str = fastapi.Query(..., alias="topic")) -> list[Gif]:
        """Get GIFs for a topic."""
        return [
            Gif(id=1, title="Gif 1", url=f"https://gif.example.com/gif1?topic={topic}"),
            Gif(id=2, title="Gif 2", url=f"https://gif.example.com/gif2?topic={topic}"),
        ]

    @app.get("/gifs/{gifId}", response_model=Gif, tags=["gifs"])
    def get_gif_by_id(gif_id: int = fastapi.Path(..., alias="gifId")) -> Gif:
        """Get GIF by Id."""
        return Gif(id=gif_id, title="Gif 1", url="https://gif.example.com/gif1")

    return app


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]  # type: ignore [no-any-return]


def run_server(app: FastAPI, host: str = "127.0.0.1", port: int = 8000) -> None:
    uvicorn.run(app, host=host, port=port)


class Server(uvicorn.Server):  # type: ignore [misc]
    def install_signal_handlers(self) -> None:
        pass

    @contextlib.contextmanager
    def run_in_thread(self) -> Iterator[None]:
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


@pytest.fixture(scope="session")
def fastapi_openapi_url(request: pytest.FixtureRequest) -> Iterator[str]:
    host = "127.0.0.1"
    port = find_free_port()
    app = request.param(host, port)
    openapi_url = f"http://{host}:{port}/openapi.json"

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = Server(config=config)
    with server.run_in_thread():
        time.sleep(1 if system() != "Windows" else 5)  # let the server start

        yield openapi_url


@pytest.fixture
def pydantic_version() -> float:
    return float(".".join(version_of_pydantic.split(".")[:2]))


################################################################################
###
# Fixtures for Agents
###
################################################################################


class InputMock:
    def __init__(self, responses: list[str]) -> None:
        """Initialize the InputMock."""
        self.responses = responses
        self.mock = MagicMock()

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        self.mock(*args, **kwargs)
        return self.responses.pop(0)


################################################################################
###
# Fixtures for Two Agent Teams
###
################################################################################

# FastAPI app for testing

################################################################################
###
# Fixtures for application
###
################################################################################
