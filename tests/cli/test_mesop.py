import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from typer.testing import CliRunner

from fastagency.cli import app

runner = CliRunner()

mesop_test = """import os

from autogen.agentchat import ConversableAgent

from fastagency import UI, FastAgency, Workflows
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI

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
def simple_workflow(
    wf: Workflows, ui: UI, initial_message: str, session_id: str
) -> str:
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

app = FastAgency(wf=wf, ui=MesopUI())
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
