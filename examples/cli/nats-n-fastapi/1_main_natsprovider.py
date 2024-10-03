import os
from os import environ

from autogen.agentchat import ConversableAgent
from fastapi import FastAPI

from fastagency import UI
from fastagency.logging import get_logger
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.nats import NatsProvider

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.0,
}

logger = get_logger(__name__)

wf = AutoGenWorkflows()


@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(
    wf: AutoGenWorkflows, ui: UI, initial_message: str, session_id: str
) -> str:
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

    logger.info("Above initiate_chat in simple_workflow")
    logger.info(llm_config)
    chat_result = student_agent.initiate_chat(
        teacher_agent,
        message=initial_message,
        summary_method="reflection_with_llm",
        max_turns=5,
    )
    logger.info("Below initiate_chat in simple_workflow")
    logger.info(chat_result)

    return chat_result.summary


nats_url = environ.get("NATS_URL", None)  # type: ignore[assignment]

user: str = "faststream"
password: str = environ.get("FASTSTREAM_NATS_PASSWORD")  # type: ignore[assignment]

provider = NatsProvider(wf=wf, nats_url=nats_url, user=user, password=password)

app = FastAPI(lifespan=provider.lifespan)


# todo: we need a way to list of workflows (names and descrioptions)
@app.get("/discover")
def start_workflow():
    # todo: you need to produce a message on NATS to actually start it

    return {"msg": "Workflow started."}


# start the provider with either command
# uvicorn main_natsprovider:app --reload