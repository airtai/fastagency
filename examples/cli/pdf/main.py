import os
from pathlib import Path
from typing import Annotated, Optional

import pymupdf4llm
from autogen import AssistantAgent, UserProxyAgent

from fastagency import UI, FastAgency, Workflows
from fastagency.base import MultipleChoice
from fastagency.logging import get_logger
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency.ui.mesop import MesopUI

logger = get_logger(__name__)

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
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
    if not initial_message:
        initial_message = "Hi! I need a help with my PDF files."

    assistant = AssistantAgent(
        name="Assistant",
        system_message="You are an assistant. Please use Markdown to format your messages. When finished, write TERMINATE in all caps to terminate the chat.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="ALWAYS",
    )

    @user_proxy.register_for_execution()
    @assistant.register_for_llm(description="List all PDF files")
    def list_pdf_files():
        files = (Path(__file__).parent / "files").glob("*.pdf")
        return list(map(str, files))

    @user_proxy.register_for_execution()
    @assistant.register_for_llm(description="Open PDF file and convert it to Markdown")
    def open_pdf_file(
        path: Annotated[str, "Full path to the PDF file"],
        pages: Annotated[
            Optional[list[int]],
            "Pages to convert. If not specified (default value), all pages will be used.",
        ] = None,
    ) -> str:
        md_text = pymupdf4llm.to_markdown(path, pages=pages)

        if len(md_text) > 20_000:
            return f"The text is too long ({len(md_text)}). Please, specify the pages to convert."

        return md_text

    files = [Path(p).stem for p in list_pdf_files()]
    file_name = ui.process_message(
        MultipleChoice(
            sender="Assistant",
            recipient="User_Proxy",
            prompt="Please, select a PDF file to open",
            choices=files,
            single=True,
        )
    )

    chat_result = user_proxy.initiate_chat(
        assistant,
        message=f"Please open the file with name {file_name} and write a summary of it in the markdown format.",
        summary_method="reflection_with_llm",
        max_turns=10,
    )

    return chat_result.summary


app = FastAgency(wf=wf, ui=MesopUI(), title="PDF Demo")
