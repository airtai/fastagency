# import json
import os
from typing import Annotated, Any, Optional

# from pathlib import Path
from autogen import register_function
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency, Workflows
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyQuery
from fastagency.base import TextInput
from fastagency.runtime.autogen.agents.websurfer import WebSurferAgent
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.console import ConsoleUI

# with Path("giphy_openapi.json").open() as f:
#     data = json.load(f)
#     openapi_json = json.dumps(data, indent=2)

# Use this for the Tutorial
# llm_config = {
#     "config_list": [
#         {
#             "model": "gpt-4o",
#             "api_key": os.getenv("OPENAI_API_KEY"),
#         }
#     ],
#     "temperature": 0.0,
# }
llm_config = {
    "config_list": [
        {
            "model": os.getenv("AZURE_GPT4_MODEL"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "base_url": os.getenv("AZURE_API_ENDPOINT"),
            "api_type": "azure",
            "api_version": "2024-02-15-preview",
        }
    ],
    "temperature": 0.0,
}

# giphy_api = OpenAPI.create(openapi_json=openapi_json)
openapi_url = "https://raw.githubusercontent.com/airtai/fastagency/refs/heads/main/examples/openapi/giphy_openapi.json"
giphy_api = OpenAPI.create(openapi_url=openapi_url)
giphy_api_key = os.getenv("GIPHY_API_KEY")

giphy_api.set_security_params(APIKeyQuery.Parameters(value=giphy_api_key))


wf = AutoGenWorkflows()

GIPHY_SYSTEM_MESSAGE = """You are an agent in charge to communicate with the user and Giphy API.
Always use 'present_completed_task_or_ask_question' to interact with the user.

Initially, the Web_Surfer_Agent will provide you with some content from the web.
You must present this content provided Web_Surfer_Agent to the user by using 'present_completed_task_or_ask_question'.
Along with the content, ask the user if he wants you to generate some gifs based on the content.

Once get the wanted gifs, present them to the user by using 'present_completed_task_or_ask_question' again.
Note: Use 'bitly_gif_url' when presenting a gif to the user.

Write 'TERMINATE' to end the conversation."""


@wf.register(name="giphy_with_security", description="Giphy chat with security")
def giphy_workflow_with_security(
    wf: Workflows, ui: UI, initial_message: str, session_id: str
) -> str:
    def is_termination_msg(msg: dict[str, Any]) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    def present_completed_task_or_ask_question(
        message: Annotated[str, "Message for examiner"],
    ) -> Optional[str]:
        try:
            msg = TextInput(
                sender="giphy_agent",
                recipient="giphy_agent",
                prompt=message,
            )
            return ui.process_message(msg)
        except Exception as e:  # pragma: no cover
            return f"present_completed_task_or_ask_question() FAILED! {e}"

    giphy_agent = ConversableAgent(
        name="Giphy_Agent",
        system_message=GIPHY_SYSTEM_MESSAGE,
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )
    web_surfer = WebSurferAgent(
        name="Web_Surfer_Agent",
        llm_config=llm_config,
        summarizer_llm_config=llm_config,
        human_input_mode="NEVER",
        executor=giphy_agent,
        is_termination_msg=is_termination_msg,
    )

    register_function(
        present_completed_task_or_ask_question,
        caller=giphy_agent,
        executor=web_surfer,
        name="present_completed_task_or_ask_question",
        description="""Present completed task or ask question.
If you are presenting a completed task, last message should be a question: 'Do yo need anything else?'""",
    )

    functions = ["random_gif", "search_gifs", "trending_gifs"]
    wf.register_api(
        api=giphy_api,
        callers=giphy_agent,
        executors=web_surfer,
        functions=functions,
    )

    chat_result = giphy_agent.initiate_chat(
        web_surfer,
        message=f"Users initial message: {initial_message}",
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(wf=wf, ui=ConsoleUI())
