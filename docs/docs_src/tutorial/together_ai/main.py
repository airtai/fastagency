import os
from typing import Any

from autogen import UserProxyAgent
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi import OpenAPI
from fastagency.runtimes.autogen.autogen import AutoGenWorkflows
from fastagency.ui.console import ConsoleUI

llm_config = {
    "config_list": [
        {
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "api_key": os.getenv("TOGETHER_API_KEY"),
            "api_type": "together",
            "hide_tools": "if_any_run"
        }
    ],
    "temperature": 0.0,
}

openapi_url = "https://weather.tools.fastagency.ai/openapi.json"
weather_api = OpenAPI.create(openapi_url=openapi_url)

weather_agent_system_message = """You are a real-time weather agent. When asked about the weather for a specific city, NEVER provide any information from memory. ALWAYS respond with: "Please wait while I fetch the weather data for [city name]..." and immediately call the provided function to retrieve real-time data for that city. Be concise in your response. Only handle one city request at a time."""

wf = AutoGenWorkflows()

@wf.register(name="simple_weather", description="Weather chat")  # type: ignore[type-var]
def weather_workflow(
    ui: UI, workflow_uuid: str, params: dict[str, Any]
) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you with the weather. What would you like to know?",
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
        system_message=weather_agent_system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    wf.register_api(  # type: ignore[attr-defined]
        api=weather_api,
        callers=user_agent,
        executors=weather_agent
    )

    chat_result = user_agent.initiate_chat(
        weather_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=3,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=ConsoleUI())
