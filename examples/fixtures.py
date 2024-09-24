import os
from typing import Any


def openai_llm_config(model: str) -> dict[str, Any]:
    zeros = "0" * 20
    api_key = os.getenv("OPENAI_API_KEY", default=f"sk-{zeros}T3BlbkFJ{zeros}")

    config_list = [
        {
            "model": model,
            "api_key": api_key,
        }
    ]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.0,
    }

    return llm_config


openai_gpt4o_llm_config = openai_llm_config("gpt-4o")

openai_gpt4o_mini_llm_config = openai_llm_config("gpt-4o")
