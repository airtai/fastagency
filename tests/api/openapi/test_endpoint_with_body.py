from typing import Any

import pytest
from autogen import ConversableAgent, UserProxyAgent
from fastapi import FastAPI
from pydantic import BaseModel

from fastagency.api.openapi.client import OpenAPI


def create_fastapi_app_with_body(host: str, port: int) -> FastAPI:
    class Item(BaseModel):
        name: str
        price: float

    app = FastAPI(
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ]
    )

    @app.post("/items")
    async def create_item(item: Item) -> str:
        return "Item created"

    return app


@pytest.mark.azure_oai
@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_fastapi_app_with_body)],
    indirect=["fastapi_openapi_url"],
)
def test_end2end(
    fastapi_openapi_url: str,
    azure_gpt35_turbo_16k_llm_config: dict[str, Any],
) -> None:
    api = OpenAPI.create(openapi_url=fastapi_openapi_url)

    agent = ConversableAgent(name="agent", llm_config=azure_gpt35_turbo_16k_llm_config)
    user_proxy = UserProxyAgent(
        name="user_proxy",
        llm_config=azure_gpt35_turbo_16k_llm_config,
        human_input_mode="NEVER",
    )

    api._register_for_llm(agent)
    api._register_for_execution(user_proxy)

    message = "Add item with name 'apple', price 1.0"
    user_proxy.initiate_chat(
        agent,
        message=message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    message_existed = False
    for message in agent.chat_messages[user_proxy]:
        if (
            isinstance(message, dict)
            and "content" in message
            and isinstance(message["content"], str)
            and message["content"] == "Item created"
        ):
            message_existed = True
            break
    assert message_existed, "Item created message not found"
