import os

from autogen.agentchat import ConversableAgent
from fastapi import FastAPI

from fastagency import UI
from fastagency.ui.console import ConsoleUI, FastAPIUI
from fastagency.runtime.autogen.base import AutoGenWorkflows

from fastagency import FastAgency
from fastagency.ui.mesop.base import MesopUI

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}


wf = AutoGenWorkflows()

@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(wf: AutoGenWorkflows, ui: UI, initial_message: str, session_id: str) -> str:
    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student willing to learn.",
        llm_config=llm_config,
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a math teacher.",
        llm_config=llm_config,
    )

    chat_result = student_agent.initiate_chat(
        teacher_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )

    return chat_result.summary


provider=FastAPIProvider(wf=wf, nats_params=..., no_workers=10)
provider=InMemoryProvider(wf=wf)


ui=MesopUI(provider=provider, )

fa_app = FastAgency(wf=wf, ui=ui)


# in case of FastAPI
app = FastAPI(lifespan=provider.lifespan())

# injects discovery routes
provider.register_app(app, discovery_path="/autogen", create_path="/workflow/create")

# ... define routes
@app.get("/workflow/create")
def create_workflow():
    return fa_app.start_workflow("simple_learning", "Hello, teacher!", "session_id")
