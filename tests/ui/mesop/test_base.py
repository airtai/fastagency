import pytest

from fastagency.app import FastAgency
from fastagency.base import TextMessage
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.mesop.base import MesopUI

# @pytest.fixture
# def mesop_import_string(
# ) -> Iterator[str]:
#     # Create a temporary file for testing
#     main_content = """
# import os

# from autogen.agentchat import ConversableAgent

# from fastagency import UI, FastAgency, Workflows
# from fastagency.runtime.autogen.base import AutoGenWorkflows
# from fastagency.ui.mesop import MesopUI

# llm_config = {
#     "config_list": [
#         {
#             "model": "gpt-4o",
#             "api_key": os.getenv("OPENAI_API_KEY"),
#         }
#     ],
#     "temperature": 0.0,
# }


# wf = AutoGenWorkflows()


# @wf.register(name="simple_learning", description="Student and teacher learning chat")
# def simple_workflow(
#     wf: Workflows, ui: UI, initial_message: str, session_id: str
# ) -> str:
#     student_agent = ConversableAgent(
#         name="Student_Agent",
#         system_message="You are a student willing to learn.",
#         llm_config=llm_config,
#     )
#     teacher_agent = ConversableAgent(
#         name="Teacher_Agent",
#         system_message="You are a math teacher.",
#         llm_config=llm_config,
#     )

#     chat_result = student_agent.initiate_chat(
#         teacher_agent,
#         message=initial_message,
#         summary_method="reflection_with_llm",
#         max_turns=5,
#     )

#     return chat_result.summary


# app = FastAgency(wf=wf, ui=MesopUI())
# """
#     init_content = """
# from .test_app import app
# """

#     with TemporaryDirectory() as tmp_dir:
#         try:
#             # save old working directory
#             old_cwd = Path.cwd()

#             # set new working directory
#             os.chdir(tmp_dir)

#             # Write the content to a temporary Python file
#             suffix = random.randint(1_000_000_000, 1_000_000_000_000 - 1)
#             mod_name = f"test-{suffix:d}"
#             app_path = Path(mod_name) / "test_app.py"
#             init_path = Path(mod_name) / "__init__.py"
#             app_path.parent.mkdir(parents=True, exist_ok=True)

#             with app_path.open("w") as f:
#                 f.write(main_content)

#             with init_path.open("w") as f:
#                 f.write(init_content)

#             # Yield control back to the tests
#             yield f"{mod_name}"
#         finally:
#             # Restore the old working directory
#             os.chdir(old_cwd)


class TestMesopUI:
    def test_mesop_init(self) -> None:
        mesop_ui = MesopUI()
        assert mesop_ui is not None
        assert mesop_ui._in_queue is not None
        assert mesop_ui._out_queue is not None

    def test_create(self) -> None:
        mesop_ui = MesopUI()
        with pytest.raises(RuntimeError, match="MesopUI has not been created yet."):
            MesopUI.get_created_instance()

        wf = AutoGenWorkflows()
        app = FastAgency(wf=wf, ui=mesop_ui)

        with mesop_ui.create(app, "import_string"):
            assert MesopUI.get_created_instance() == mesop_ui
            assert mesop_ui.app == app

    def test_mesop_mesage(self) -> None:
        mesop_ui = MesopUI()

        io_msg = TextMessage(
            sender="sender",
            recipient="recipient",
            body="message",
        )

        mesop_msg = mesop_ui._mesop_message(io_msg)
        assert mesop_msg.conversation == mesop_ui
        assert mesop_msg.io_message == io_msg
