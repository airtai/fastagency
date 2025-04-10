import pytest
from autogen import ConversableAgent, LLMConfig, UserProxyAgent
from fastapi import FastAPI
from pydantic import BaseModel

from fastagency.api.openapi import OpenAPI


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
    fastapi_openapi_url: str, azure_gpt35_turbo_16k_llm_config: LLMConfig
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
    response = user_proxy.run(
        agent,
        message=message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    events = []
    for event in response.events:
        events.append(event)

        if event.type == "input_request":
            event.content.respond("exit")

    message_existed = False
    expected_message = "Item created"
    message_contents: list[str] = []
    for message in response.messages:
        if (
            isinstance(message, dict)
            and "content" in message
            and isinstance(message["content"], str)
            and message["content"] == expected_message
        ):
            message_contents.append(message.get("content", ""))
            message_existed = True
            break
    assert message_existed, (
        f"Expected message '{expected_message}' not found in {message_contents} {events}"
    )
