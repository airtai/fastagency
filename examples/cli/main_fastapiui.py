import os

from autogen.agentchat import ConversableAgent

from fastagency import UI
from fastagency.runtime.autogen.base import AutoGenWorkflows

from fastagency import FastAgency

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

# ui=FastAPIUI(nats_params=..., no_workers=10)
# fa_app = FastAgency(wf=wf, ui=ui)

# app = FastAPI(lifespan=fa_app.lifespan(fa_app))

# # do whatever you want with the app
# ...
# def some_route():
#     web_socket_info = fa_app.run_workflow("simple_learning", "Hello, teacher!", "session_id")

from fastagency.ui.fastapi.base import FastAPIUI
from fastapi import FastAPI

ui = FastAPIUI()
fa_app = FastAgency(wf=wf, ui=ui)

app = FastAPI(lifespan=ui.lifespan)
app.include_router(ui.router)
