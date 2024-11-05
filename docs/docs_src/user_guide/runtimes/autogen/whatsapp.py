import os
from typing import Annotated, Any, Optional

from autogen import GroupChat, GroupChatManager, register_function
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.runtimes.autogen import AutoGenWorkflows
from fastagency.runtimes.autogen.agents.websurfer import WebSurferAgent
from fastagency.runtimes.autogen.agents.whatsapp import WhatsAppAgent
from fastagency.ui.mesop import MesopUI


EXECUTOR_AGENT_SYSTEM_MESSAGE = """You are an agent in charge of communication with the user, the WhatsApp_Agent, and Web_Surfer_Agent.
Always use 'present_completed_task_or_ask_question' to interact with the user.
- make sure that the 'message' parameter contains all the necessary information for the user!
Initially, the Web_Surfer_Agent will provide you with some content from the web.
You should ask the user if he would like to receive the summary of the scraped page
by using 'present_completed_task_or_ask_question'.
- "If you want to receive the summary of the page as a WhatsApp message, please provide your number."

After that, relay the work to WhatsApp_Agent to send the message to the user"""

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

wf = AutoGenWorkflows()


@wf.register(name="whatsapp_and_websurfer", description="WhatsApp and WebSurfer chat")
def whatsapp_and_websurfer_workflow(ui: UI, params: dict[str, Any]) -> str:
    def is_termination_msg(msg: dict[str, Any]) -> bool:
        return msg["content"] is not None and "TERMINATE" in msg["content"]

    def present_completed_task_or_ask_question(
        message: Annotated[str, "Message for user"],
    ) -> Optional[str]:
        try:
            return ui.text_input(
                sender="Executor_Agent",
                recipient="User",
                prompt=message,
            )
        except Exception as e:  # pragma: no cover
            return f"present_completed_task_or_ask_question() FAILED! {e}"

    executor_agent = ConversableAgent(
        name="Executor_Agent",
        system_message=EXECUTOR_AGENT_SYSTEM_MESSAGE,
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    whatsapp_agent = WhatsAppAgent(
        name="WhatsApp_Agent",
        # This is the default sender number for Infobip.
        # If you want to use your own sender, please update the value below:
        sender = "447860099299",
        llm_config=llm_config,
        human_input_mode="NEVER",
        executor=executor_agent,
        is_termination_msg=is_termination_msg,
        whatsapp_api_key=os.getenv("WHATSAPP_API_KEY"),
    )

    web_surfer = WebSurferAgent(
        name="Web_Surfer_Agent",
        llm_config=llm_config,
        summarizer_llm_config=llm_config,
        human_input_mode="NEVER",
        executor=executor_agent,
        is_termination_msg=is_termination_msg,
        bing_api_key=os.getenv("BING_API_KEY"),
    )

    register_function(
        present_completed_task_or_ask_question,
        caller=executor_agent,
        executor=web_surfer,
        name="present_completed_task_or_ask_question",
        description="""Present completed task or ask question.
If you are presenting a completed task, last message should be a question: 'Do you need anything else?'""",
    )


    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="For which website would you like to receive a summary?",
    )

    group_chat = GroupChat(
        agents=[executor_agent, whatsapp_agent, web_surfer],
        messages=[],
        max_round=20,
    )

    group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    chat_result = executor_agent.initiate_chat(
        group_chat_manager,
        message=initial_message,
        summary_method="reflection_with_llm",
    )

    return chat_result.summary  # type: ignore[no-any-return]


app = FastAgency(provider=wf, ui=MesopUI(), title="WhatsApp chat")
