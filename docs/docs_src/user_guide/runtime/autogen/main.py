import os

from autogen import UserProxyAgent
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi import OpenAPI
from fastagency.runtime.autogen.base import AutoGenWorkflows
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

openapi_url = "https://weather.tools.fastagency.ai/openapi.json"

weather_api = OpenAPI.create(openapi_url=openapi_url)

wf = AutoGenWorkflows()


@wf.register(name="simple_weather", description="Weather chat")  # type: ignore[type-var]
def weather_workflow(
    wf: AutoGenWorkflows, ui: UI, initial_message: str, session_id: Optional[UUID] = None
) -> str:
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

    wf.register_api(  # type: ignore[attr-defined]
        api=weather_api,
        callers=[user_agent],
        executors=[weather_agent],
        functions=[
            {
                "get_daily_weather_daily_get": {
                    "name": "get_daily_weather",
                    "description": "Get the daily weather",
                }
            },
            "get_hourly_weather_hourly_get",
        ],
    )

    chat_result = user_agent.initiate_chat(
        weather_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI())
