import os
from typing import Annotated, Any, Optional

from autogen import register_function
from autogen.agentchat import ConversableAgent

from fastagency import UI
from fastagency.api.openapi import OpenAPI
from fastagency.api.openapi.security import APIKeyQuery
from fastagency.runtimes.ag2.agents.websurfer import WebSurferAgent
from fastagency.runtimes.ag2 import Workflow

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

openapi_url = "https://raw.githubusercontent.com/ag2ai/fastagency/refs/heads/main/examples/openapi/giphy_openapi.json"
giphy_api = OpenAPI.create(openapi_url=openapi_url)

giphy_api_key = os.getenv("GIPHY_API_KEY", "")
giphy_api.set_security_params(APIKeyQuery.Parameters(value=giphy_api_key))

GIPHY_SYSTEM_MESSAGE = """You are an agent in charge to communicate with the user and Giphy API.
Always use 'present_completed_task_or_ask_question' to interact with the user.
- make sure that the 'message' parameter contains all the necessary information for the user!
Initially, the Web_Surfer_Agent will provide you with some content from the web.
You must present this content provided Web_Surfer_Agent to the user by using 'present_completed_task_or_ask_question'.
Along with the content, ask the user if he wants you to generate some gifs based on the content.
- Do NOT generate gifs BEFORE you present the web content to the user, otherwise, you will be penalized!

Once get the wanted gifs, present them to the user by using 'present_completed_task_or_ask_question' again.
Note: Use '.gif' files when presenting a gif to the user and format it as a markdown gif -> ![Title](url)
- Also, make sure to add new lines '\n\n' between headlines and gifs for better readability.
e.g.:
'''
# Here are some gifs for you:

## Title 1
![Title 1](url1)

## Title 2
![Title 2](url2)
'''

Write 'TERMINATE' to end the conversation."""

wf = Workflow()


@wf.register(name="giphy_and_websurfer", description="Giphy and Websurfer chat")
def giphy_workflow_with_security(
    ui: UI, params: dict[str, Any]
) -> str:
    def is_termination_msg(msg: dict[str, Any]) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    def present_completed_task_or_ask_question(
        message: Annotated[str, "Message for examiner"],
    ) -> Optional[str]:
        try:
            return ui.text_input(
                sender="giphy_agent",
                recipient="giphy_agent",
                prompt=message,
            )
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
        bing_api_key=os.getenv("BING_API_KEY")
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

    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you find images related to a certain subject. What kind of images would you like to find?",
    )

    run_response = giphy_agent.run(
        web_surfer,
        message=f"Users initial message: {initial_message}",
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return run_response.summary  # type: ignore[no-any-return]
