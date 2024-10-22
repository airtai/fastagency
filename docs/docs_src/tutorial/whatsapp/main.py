import os
from typing import Annotated, Any, Optional

from autogen import register_function
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.api.openapi.client import OpenAPI
from fastagency.api.openapi.security import APIKeyHeader
from fastagency.runtimes.autogen.agents.websurfer import WebSurferAgent
from fastagency.runtimes.autogen.autogen import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

openapi_url = "https://raw.githubusercontent.com/airtai/fastagency/refs/heads/main/examples/openapi/whatsapp_openapi.json"
whatsapp_api = OpenAPI.create(
    openapi_url=openapi_url,
)

header_authorization = "App "  # pragma: allowlist secret
header_authorization += os.getenv("WHATSAPP_API_KEY", "")
whatsapp_api.set_security_params(APIKeyHeader.Parameters(value=header_authorization))

WHATSAPP_SYSTEM_MESSAGE = """You are an agent in charge to communicate with the user and WhatsAPP API.
Always use 'present_completed_task_or_ask_question' to interact with the user.
- make sure that the 'message' parameter contains all the necessary information for the user!
Initially, the Web_Surfer_Agent will provide you with some content from the web.
You should ask the user if he would like to receive the summary of the scraped page
by using 'present_completed_task_or_ask_question'.
- "If you want to receive the summary of the page as a WhatsApp message, please provide your number."

    When sending the message, the Body must use the following format:
{
    "from": "447860099299",
    "to": "receiverNumber",
    "messageId": "test-message-randomInt",
    "content": {
        "text": "message"
    },
    "callbackData": "Callback data"
}

"from" number is always the same.
"""

wf = AutoGenWorkflows()


@wf.register(name="whatsapp", description="WhatsApp chat")
def whatsapp_workflow(ui: UI, params: dict[str, Any]) -> str:
    def is_termination_msg(msg: dict[str, Any]) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    def present_completed_task_or_ask_question(
        message: Annotated[str, "Message for examiner"],
    ) -> Optional[str]:
        try:
            return ui.text_input(
                sender="Whatsapp_Agent",
                recipient="User",
                prompt=message,
            )
        except Exception as e:  # pragma: no cover
            return f"present_completed_task_or_ask_question() FAILED! {e}"

    whatsapp_agent = ConversableAgent(
        name="Whatsapp_Agent",
        system_message=WHATSAPP_SYSTEM_MESSAGE,
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    web_surfer = WebSurferAgent(
        name="Web_Surfer_Agent",
        llm_config=llm_config,
        summarizer_llm_config=llm_config,
        human_input_mode="NEVER",
        executor=whatsapp_agent,
        is_termination_msg=is_termination_msg,
    )

    register_function(
        present_completed_task_or_ask_question,
        caller=whatsapp_agent,
        executor=web_surfer,
        name="present_completed_task_or_ask_question",
        description="""Present completed task or ask question.
If you are presenting a completed task, last message should be a question: 'Do yo need anything else?'""",
    )

    wf.register_api(
        api=whatsapp_api,
        callers=whatsapp_agent,
        executors=web_surfer,
    )

    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="For which website would you like to receive a summary?",
    )

    chat_result = whatsapp_agent.initiate_chat(
        web_surfer,
        message=f"Users initial message: {initial_message}",
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=MesopUI(), title="WhatsApp chat")
