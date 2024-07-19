from typing import Annotated, Any, Dict, Literal
from uuid import UUID

from pydantic import AfterValidator, Field, HttpUrl
from typing_extensions import TypeAlias

from ..base import Model
from ..registry import register

__all__ = [
    "TogetherAIAPIKey",
    "TogetherAI",
]

# retrieve the models from the API on July 19, 2024
together_model_string = {
    "WizardLM v1.2 (13B)": "WizardLM/WizardLM-13B-V1.2",
    "Code Llama Instruct (34B)": "togethercomputer/CodeLlama-34b-Instruct",
    "Upstage SOLAR Instruct v1 (11B)": "upstage/SOLAR-10.7B-Instruct-v1.0",
    "OpenHermes-2-Mistral (7B)": "teknium/OpenHermes-2-Mistral-7B",
    "LLaMA-2-7B-32K-Instruct (7B)": "togethercomputer/Llama-2-7B-32K-Instruct",
    "ReMM SLERP L2 (13B)": "Undi95/ReMM-SLERP-L2-13B",
    "Toppy M (7B)": "Undi95/Toppy-M-7B",
    "OpenChat 3.5": "openchat/openchat-3.5-1210",
    "Chronos Hermes (13B)": "Austism/chronos-hermes-13b",
    "Snorkel Mistral PairRM DPO (7B)": "snorkelai/Snorkel-Mistral-PairRM-DPO",
    "Qwen 1.5 Chat (7B)": "Qwen/Qwen1.5-7B-Chat",
    "Qwen 1.5 Chat (14B)": "Qwen/Qwen1.5-14B-Chat",
    "Qwen 1.5 Chat (1.8B)": "Qwen/Qwen1.5-1.8B-Chat",
    "Snowflake Arctic Instruct": "Snowflake/snowflake-arctic-instruct",
    "Code Llama Instruct (70B)": "codellama/CodeLlama-70b-Instruct-hf",
    "Nous Hermes 2 - Mixtral 8x7B-SFT": "NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT",
    "Dolphin 2.5 Mixtral 8x7b": "cognitivecomputations/dolphin-2.5-mixtral-8x7b",
    "Nous Hermes 2 - Mixtral 8x7B-DPO ": "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    "Mixtral-8x22B Instruct v0.1": "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "Deepseek Coder Instruct (33B)": "deepseek-ai/deepseek-coder-33b-instruct",
    "Nous Hermes Llama-2 (13B)": "NousResearch/Nous-Hermes-Llama2-13b",
    "Vicuna v1.5 (13B)": "lmsys/vicuna-13b-v1.5",
    "Qwen 1.5 Chat (0.5B)": "Qwen/Qwen1.5-0.5B-Chat",
    "Code Llama Instruct (7B)": "togethercomputer/CodeLlama-7b-Instruct",
    "Nous Hermes-2 Yi (34B)": "NousResearch/Nous-Hermes-2-Yi-34B",
    "Code Llama Instruct (13B)": "togethercomputer/CodeLlama-13b-Instruct",
    "Llama3 8B Chat HF INT4": "togethercomputer/Llama-3-8b-chat-hf-int4",
    "OpenHermes-2.5-Mistral (7B)": "teknium/OpenHermes-2p5-Mistral-7B",
    "Nous Capybara v1.9 (7B)": "NousResearch/Nous-Capybara-7B-V1p9",
    "Nous Hermes 2 - Mistral DPO (7B)": "NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
    "StripedHyena Nous (7B)": "togethercomputer/StripedHyena-Nous-7B",
    "Alpaca (7B)": "togethercomputer/alpaca-7b",
    "Platypus2 Instruct (70B)": "garage-bAInd/Platypus2-70B-instruct",
    "Gemma Instruct (2B)": "google/gemma-2b-it",
    "Gemma Instruct (7B)": "google/gemma-7b-it",
    "OLMo Instruct (7B)": "allenai/OLMo-7B-Instruct",
    "Qwen 1.5 Chat (4B)": "Qwen/Qwen1.5-4B-Chat",
    "MythoMax-L2 (13B)": "Gryphe/MythoMax-L2-13b",
    "Meta Llama 3 70B Reference": "meta-llama/Llama-3-70b-chat-hf",
    "Mistral (7B) Instruct": "mistralai/Mistral-7B-Instruct-v0.1",
    "Mistral (7B) Instruct v0.2": "mistralai/Mistral-7B-Instruct-v0.2",
    "OpenOrca Mistral (7B) 8K": "Open-Orca/Mistral-7B-OpenOrca",
    "Nous Hermes LLaMA-2 (7B)": "NousResearch/Nous-Hermes-llama-2-7b",
    "Qwen 1.5 Chat (32B)": "Qwen/Qwen1.5-32B-Chat",
    "Qwen 2 Instruct (72B)": "Qwen/Qwen2-72B-Instruct",
    "Qwen 1.5 Chat (72B)": "Qwen/Qwen1.5-72B-Chat",
    "DeepSeek LLM Chat (67B)": "deepseek-ai/deepseek-llm-67b-chat",
    "Vicuna v1.5 (7B)": "lmsys/vicuna-7b-v1.5",
    "WizardLM-2 (8x22B)": "microsoft/WizardLM-2-8x22B",
    "Togethercomputer Llama3 8B Instruct Int8": "togethercomputer/Llama-3-8b-chat-hf-int8",
    "Mistral (7B) Instruct v0.3": "mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen 1.5 Chat (110B)": "Qwen/Qwen1.5-110B-Chat",
    "LLaMA-2 Chat (13B)": "togethercomputer/llama-2-13b-chat",
    "Gemma-2 Instruct (27B)": "google/gemma-2-27b-it",
    "01-ai Yi Chat (34B)": "zero-one-ai/Yi-34B-Chat",
    "Meta Llama 3 70B Instruct Turbo": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
    "Meta Llama 3 8B Instruct Turbo": "meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
    "Meta Llama 3 70B Instruct Lite": "meta-llama/Meta-Llama-3-70B-Instruct-Lite",
    "Gemma-2 Instruct (9B)": "google/gemma-2-9b-it",
    "Meta Llama 3 8B Instruct Lite": "meta-llama/Meta-Llama-3-8B-Instruct-Lite",
    "Meta Llama 3 8B Reference": "meta-llama/Llama-3-8b-chat-hf",
    "Mixtral-8x7B Instruct v0.1": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "LLaMA-2 Chat (7B)": "togethercomputer/llama-2-7b-chat",
    "LLaMA-2 Chat (70B)": "togethercomputer/llama-2-70b-chat",
    "Reserved - DBRX Instruct": "medaltv/dbrx-instruct",
    "DBRX Instruct": "databricks/dbrx-instruct",
    "Koala (7B)": "togethercomputer/Koala-7B",
    "Guanaco (65B) ": "togethercomputer/guanaco-65b",
    "Vicuna v1.3 (7B)": "lmsys/vicuna-7b-v1.3",
    "Nous Hermes LLaMA-2 (70B)": "NousResearch/Nous-Hermes-Llama2-70b",
    "Vicuna v1.5 16K (13B)": "lmsys/vicuna-13b-v1.5-16k",
    "Zephyr-7B-ß": "HuggingFaceH4/zephyr-7b-beta",
    "Guanaco (13B) ": "togethercomputer/guanaco-13b",
    "Vicuna v1.3 (13B)": "lmsys/vicuna-13b-v1.3",
    "Guanaco (33B) ": "togethercomputer/guanaco-33b",
    "Koala (13B)": "togethercomputer/Koala-13B",
    "Upstage SOLAR Instruct v1 (11B)-Int4": "togethercomputer/SOLAR-10.7B-Instruct-v1.0-int4",
    "Guanaco (7B) ": "togethercomputer/guanaco-7b",
    "Meta Llama 3 8B Instruct": "meta-llama/Meta-Llama-3-8B-Instruct",
    "Meta Llama 3 70B Instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    "Hermes 2 Theta Llama-3 70B": "NousResearch/Hermes-2-Theta-Llama-3-70B",
    "Llama-3 70B Instruct Gradient 1048K": "gradientai/Llama-3-70B-Instruct-Gradient-1048k",
}

TogetherModels: TypeAlias = Literal[tuple(together_model_string.keys())]  # type: ignore[valid-type]


@register("secret")
class TogetherAIAPIKey(Model):
    api_key: Annotated[
        str,
        Field(
            description="The API Key from Together.ai",
            min_length=64,
            max_length=64,
        ),
    ]

    @classmethod
    async def create_autogen(cls, model_id: UUID, user_id: UUID, **kwargs: Any) -> str:
        my_model: TogetherAIAPIKey = await cls.from_db(model_id)

        return my_model.api_key


TogetherAIAPIKeyRef: TypeAlias = TogetherAIAPIKey.get_reference_model()  # type: ignore[valid-type]

# Pydantic adds trailing slash automatically to URLs, so we need to remove it
# https://github.com/pydantic/pydantic/issues/7186#issuecomment-1691594032
URL = Annotated[HttpUrl, AfterValidator(lambda x: str(x).rstrip("/"))]


@register("llm")
class TogetherAI(Model):
    model: Annotated[  # type: ignore[valid-type]
        TogetherModels,
        Field(description="The model to use for the Together API"),
    ] = "Meta Llama 3 70B Reference"

    api_key: TogetherAIAPIKeyRef

    base_url: Annotated[URL, Field(description="The base URL of the OpenAI API")] = URL(
        url="https://api.together.xyz/v1"
    )

    api_type: Annotated[
        Literal["togetherai"],
        Field(
            title="API Type", description="The type of the API, must be 'togetherai'"
        ),
    ] = "togetherai"

    temperature: Annotated[
        float,
        Field(
            description="The temperature to use for the model, must be between 0 and 2",
            ge=0.0,
            le=2.0,
        ),
    ] = 0.8

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> Dict[str, Any]:
        my_model: TogetherAI = await cls.from_db(model_id)

        api_key_model: TogetherAIAPIKey = (
            await my_model.api_key.get_data_model().from_db(my_model.api_key.uuid)
        )

        api_key = await api_key_model.create_autogen(my_model.api_key.uuid, user_id)

        config_list = [
            {
                "model": together_model_string[my_model.model],
                "api_key": api_key,
                "base_url": str(my_model.base_url),
                "api_type": my_model.api_type,
            }
        ]

        llm_config = {
            "config_list": config_list,
            "temperature": my_model.temperature,
        }

        return llm_config
