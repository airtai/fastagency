# WhatsApp Agent

The WhatsApp Agent within FastAgency allows users to send messages via WhatsApp by integrating it seamlessly with other agents, such as the WebSurfer Agent. This setup can help users retrieve web-based information and deliver summaries directly to their WhatsApp.

## Adding WhatsApp Capabilities to Agents

There are two main ways to integrate WhatsApp messaging:

1. Use a **WhatsAppAgent** to send messages directly to WhatsApp (recommended).
2. Combine it with other agents, such as a WebSurferAgent, to provide dynamic, web-enhanced WhatsApp interactions.

In this guide, we’ll walk through a workflow where users can request a web page summary, which is then relayed to their WhatsApp.

## Installation & Setup

First, make sure you have FastAgency installed with the following command:

\```bash
pip install "fastagency[autogen]"
\```

This command installs FastAgency with Console and AutoGen runtime support.

## Environment Setup

You need to set up your API keys for Bing Web Search and WhatsApp. Ensure you have an account with **Microsoft Azure** to obtain a Bing API key and with your WhatsApp API provider.

### Set Up Your API Keys

You can set the API keys as environment variables in your terminal:

=== "Linux/macOS"
    \```bash
    export BING_API_KEY="your_bing_api_key"
    export WHATSAPP_API_KEY="your_whatsapp_api_key"
    \```

=== "Windows"
    \```bash
    set BING_API_KEY="your_bing_api_key"
    set WHATSAPP_API_KEY="your_whatsapp_api_key"
    \```

## Example: Send a Web Summary to WhatsApp

### Step-by-Step Guide

#### 1. **Import Required Modules**

First, import the required modules from **AutoGen** and **FastAgency**. This example combines the **WhatsAppAgent** and **WebSurferAgent** to retrieve web information and send it via WhatsApp.

\```python
import os
from typing import Annotated, Any, Optional

from autogen import GroupChat, GroupChatManager, register_function
from autogen.agentchat import ConversableAgent
from fastagency import UI, FastAgency
from fastagency.runtimes.autogen import AutoGenWorkflows
from fastagency.runtimes.autogen.agents.websurfer import WebSurferAgent
from fastagency.runtimes.autogen.agents.whatsapp import WhatsAppAgent
from fastagency.ui.mesop import MesopUI
\```

#### 2. **Define the System Message for the Executor Agent**

The **Executor Agent** manages communication between the user, WhatsAppAgent, and WebSurferAgent.

\```python
EXECUTOR_AGENT_SYSTEM_MESSAGE = """You are an agent in charge of communication with the user, the WhatsApp_Agent, and Web_Surfer_Agent.
Always use 'present_completed_task_or_ask_question' to interact with the user.
- Make sure that the 'message' parameter contains all the necessary information for the user.
Initially, the Web_Surfer_Agent will provide you with some content from the web.
You should ask the user if they would like to receive the summary of the scraped page.
- "If you want to receive the summary of the page as a WhatsApp message, please provide your number."
After that, relay the work to WhatsApp_Agent to send the message to the user."""
\```

#### 3. **Configure the Language Model (LLM)**

Define the LLM configuration with **gpt-4o-mini** model and retrieve the OpenAI API key from the environment.

\```python
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}
\```

#### 4. **Define the Workflow**

Register a workflow to enable interaction with both WhatsApp and WebSurfer agents.

\```python
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
        except Exception as e:
            return f"present_completed_task_or_ask_question() FAILED! {e}"
\```

#### 5. **Set Up the Agents**

Initialize the Executor Agent, WhatsApp Agent, and Web Surfer Agent.

\```python
    executor_agent = ConversableAgent(
        name="Executor_Agent",
        system_message=EXECUTOR_AGENT_SYSTEM_MESSAGE,
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    whatsapp_agent = WhatsAppAgent(
        name="WhatsApp_Agent",
        sender="447860099299",  # default sender number for Infobip
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
\```

#### 6. **Register the Task Presentation Function**

The **Executor Agent** uses this function to relay task information to the user.

\```python
    register_function(
        present_completed_task_or_ask_question,
        caller=executor_agent,
        executor=web_surfer,
        name="present_completed_task_or_ask_question",
        description="""Present completed task or ask question.
If you are presenting a completed task, last message should be a question: 'Do you need anything else?'""",
    )
\```

#### 7. **Set Up the Initial Message and Group Chat**

The user can input the URL they’d like summarized, which the agents then process and deliver via WhatsApp.

\```python
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

    return chat_result.summary
\```

#### 8. **Create and Run the Application**

Finally, initialize the FastAgency application with the `whatsapp_and_websurfer_workflow` and launch the app.

\```python
app = FastAgency(provider=wf, ui=MesopUI(), title="WhatsApp chat")
\```

## Running the Application

To start the application, run:

\```bash
fastagency run whatsapp_and_websurfer.py
\```

The system will prompt the user for a URL and process the request, with the summary sent directly to their WhatsApp.

---

This example demonstrates how to leverage FastAgency’s AutoGen runtime to integrate WhatsApp and web-surfing functionalities, allowing for rich, real-time messaging experiences.