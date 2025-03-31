import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from typer.testing import CliRunner

from fastagency.cli import app

runner = CliRunner()

mesop_test = """import os

from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency, WorkflowsProtocol
from fastagency.runtimes.ag2 import Workflow
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

wf = Workflow()

@wf.register(name="simple_learning", description="Student and teacher learning chat")
def simple_workflow(
    ui: UI, workflow_uuid: str, params: dict[str, Any]
) -> str:
    initial_message = ui.text_input(
        sender="Workflow",
        recipient="User",
        prompt="I can help you learn about mathematics. What subject you would like to explore?",
        workflow_uuid=workflow_uuid,
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

    return chat_result.summary

app = FastAgency(provider=wf, ui=MesopUI())
"""


@pytest.mark.skipif(
    sys.version_info >= (3, 10), reason="Python 3.10 or higher is required"
)
def test_app_failure_for_python39() -> None:
    """Test that the app fails when Python 3.9 is used."""
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / "main_mesop.py"
        with tmp_path.open("w") as f:
            f.write(mesop_test)

        result = runner.invoke(app, ["run", str(tmp_path)])

        assert result.exit_code == 1

        assert "Mesop requires Python 3.10 or higher" in result.output
