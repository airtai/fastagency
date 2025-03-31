import os
from typing import Any

import mesop as me
from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency
from fastagency.runtimes.ag2 import Workflow
from fastagency.ui.mesop import MesopUI
from fastagency.ui.mesop.auth.firebase import FirebaseAuth, FirebaseConfig
from fastagency.ui.mesop.styles import (
    MesopHomePageStyles,
    MesopMessagesStyles,
    MesopSingleChoiceInnerStyles,
)

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.8,
}

wf = Workflow()


@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(
    ui: UI, params: dict[str, Any]
) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="What do you want to learn today?",
    )

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

    return chat_result.summary  # type: ignore[no-any-return]


security_policy=me.SecurityPolicy(allowed_iframe_parents=["https://acme.com"], allowed_script_srcs=["https://cdn.jsdelivr.net"])

styles=MesopHomePageStyles(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
    ],
    root=me.Style(
        background="#e7f2ff",
        height="100%",
        font_family="Inter",
        display="flex",
        flex_direction="row",
    ),
    message=MesopMessagesStyles(
        single_choice_inner=MesopSingleChoiceInnerStyles(
            disabled_button=me.Style(
                margin=me.Margin.symmetric(horizontal=8),
                padding=me.Padding.all(16),
                border_radius=8,
                background="#64b5f6",
                color="#fff",
                font_size=16,
            ),
        )
    ),
)

# TODO: replace this with your web app's Firebase configuration
firebase_config = FirebaseConfig(
    api_key="<your_firebase_api_key>",
    auth_domain="<your_firebase_auth_domain>",
    project_id="<your_firebase_project_id>",
    storage_bucket="<your_firebase_storage_bucket>",
    messaging_sender_id="<your_firebase_messaging_sender_id>",
    app_id="<your_firebase_app_id>"
)

# Initialize auth with Google sign-in
auth = FirebaseAuth(
    sign_in_methods=["google"],
    config=firebase_config,
    # TODO: Replace the emails in allowed_users with the desired ones
    allowed_users=["harish@airt.ai", "davor@airt.ai"]
)

ui = MesopUI(security_policy=security_policy, styles=styles, auth=auth)

app = FastAgency(provider=wf, ui=ui, title="Learning Chat")
