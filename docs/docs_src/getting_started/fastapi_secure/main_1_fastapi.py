import os
from typing import Any
from uuid import UUID, uuid4

from autogen.agentchat import ConversableAgent
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import APIKeyHeader

from fastagency import UI
from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.runtimes.autogen import AutoGenWorkflows

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


@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(ui: UI, params: dict[str, Any]) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you learn about mathematics. What subject you would like to explore?",
    )

    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student willing to learn.",
        llm_config=llm_config,
        # human_input_mode="ALWAYS",
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a math teacher.",
        llm_config=llm_config,
        # human_input_mode="ALWAYS",
    )

    chat_result = student_agent.initiate_chat(
        teacher_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )

    return chat_result.summary  # type: ignore[no-any-return]

# Prepare fastapi function for checking API key (mocked)
api_key_header = APIKeyHeader(name="X-API-Key")

def get_user_id(api_key_header: str = Depends(api_key_header)) -> UUID:
        if api_key_header == "api_key":  # pragma: allowlist secret
            return uuid4()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

adapter = FastAPIAdapter(
    provider=wf,
    get_user_id = get_user_id
)

app = FastAPI()
app.include_router(adapter.router)


# this is optional, but we would like to see the list of available workflows
@app.get("/")
def read_root() -> dict[str, dict[str, str]]:
    return {"Workflows": {name: wf.get_description(name) for name in wf.names}}


# start the provider with the following command
# uvicorn main_1_fastapi:app --host 0.0.0.0 --port 8008 --reload
