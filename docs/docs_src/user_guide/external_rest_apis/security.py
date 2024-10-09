import os

from autogen import UserProxyAgent
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtimes.autogen.autogen import AutoGenWorkflows
from fastagency.ui.console import ConsoleUI

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}

WEATHER_OPENAPI_URL = "https://weather.tools.fastagency.ai/openapi.json"
weather_api = OpenAPI.create(openapi_url=WEATHER_OPENAPI_URL)

# Set global security params for all methods
weather_api.set_security_params(APIKeyHeader.Parameters(value="secure weather key"))

# Set security params for a specific method
# weather_api.set_security_params(
#     APIKeyHeader.Parameters(value="secure weather key"),
#     "get_daily_weather_daily_get",
# )

wf = AutoGenWorkflows()


@wf.register(
    name="simple_weather_with_security", description="Weather chat with security"
)
def weather_workflow_with_security(
    ui: UI, workflow_uuid: str, params: dict[str, str]
) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="What do you want to know about the weather?",
        workflow_uuid=workflow_uuid,
    )

    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    weather_agent = ConversableAgent(
        name="Weather_Agent",
        system_message="You are a weather agent",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    wf.register_api(
        api=weather_api,
        callers=user_agent,
        executors=weather_agent,
    )

    chat_result = user_agent.initiate_chat(
        weather_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI())
