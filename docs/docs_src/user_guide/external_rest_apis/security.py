import os

from autogen import UserProxyAgent, ConversableAgent, LLMConfig

from fastagency import UI, FastAgency
from fastagency.api.openapi import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtimes.ag2 import Workflow
from fastagency.ui.console import ConsoleUI

llm_config = LLMConfig(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.8,
)

WEATHER_OPENAPI_URL = "https://weather.tools.fastagency.ai/openapi.json"
weather_api = OpenAPI.create(openapi_url=WEATHER_OPENAPI_URL)

# Set global security params for all methods
weather_api.set_security_params(APIKeyHeader.Parameters(value="secure weather key"))

# Set security params for a specific method
# weather_api.set_security_params(
#     APIKeyHeader.Parameters(value="secure weather key"),
#     "get_daily_weather_daily_get",
# )

wf = Workflow()


@wf.register(
    name="simple_weather_with_security", description="Weather chat with security"
)
def weather_workflow_with_security(
    ui: UI, params: dict[str, str]
) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="What do you want to know about the weather?",
    )

    user_agent = UserProxyAgent(
        name="User_Agent",
        system_message="You are a user agent",
        human_input_mode="NEVER",
        llm_config=llm_config,
    )
    weather_agent = ConversableAgent(
        name="Weather_Agent",
        system_message="You are a weather agent",
        human_input_mode="NEVER",
        llm_config=llm_config,
    )

    wf.register_api(
        api=weather_api,
        callers=user_agent,
        executors=weather_agent,
    )

    response = user_agent.run(
        weather_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return ui.process(response)  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI())
