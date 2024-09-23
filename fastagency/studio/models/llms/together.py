from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import AfterValidator, HttpUrl
from typing_extensions import TypeAlias

from ..base import Field, Model
from ..registry import register

__all__ = [
    "TogetherAIAPIKey",
    "TogetherAI",
]

# retrieve the models from the API on July 19, 2024
together_model_string = {
    "Code Llama Instruct (34B)": "togethercomputer/CodeLlama-34b-Instruct",
    "Upstage SOLAR Instruct v1 (11B)": "upstage/SOLAR-10.7B-Instruct-v1.0",
    "Nous Hermes-2 Yi (34B)": "NousResearch/Nous-Hermes-2-Yi-34B",
    "Llama3 8B Chat HF INT4": "togethercomputer/Llama-3-8b-chat-hf-int4",
    "StripedHyena Nous (7B)": "togethercomputer/StripedHyena-Nous-7B",
    "Gemma Instruct (2B)": "google/gemma-2b-it",
    "MythoMax-L2 (13B)": "Gryphe/MythoMax-L2-13b",
    "Mistral (7B) Instruct": "mistralai/Mistral-7B-Instruct-v0.1",
    "Mistral (7B) Instruct v0.2": "mistralai/Mistral-7B-Instruct-v0.2",
    "Qwen 2 Instruct (72B)": "Qwen/Qwen2-72B-Instruct",
    "Qwen 1.5 Chat (72B)": "Qwen/Qwen1.5-72B-Chat",
    "DeepSeek LLM Chat (67B)": "deepseek-ai/deepseek-llm-67b-chat",
    "Togethercomputer Llama3 8B Instruct Int8": "togethercomputer/Llama-3-8b-chat-hf-int8",
    "Mistral (7B) Instruct v0.3": "mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen 1.5 Chat (110B)": "Qwen/Qwen1.5-110B-Chat",
    "LLaMA-2 Chat (13B)": "togethercomputer/llama-2-13b-chat",
    "Gemma-2 Instruct (27B)": "google/gemma-2-27b-it",
    "Meta Llama 3 70B Instruct Turbo": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
    "Meta Llama 3 70B Instruct Lite": "meta-llama/Meta-Llama-3-70B-Instruct-Lite",
    "Gemma-2 Instruct (9B)": "google/gemma-2-9b-it",
    "Meta Llama 3 8B Instruct Reference": "meta-llama/Llama-3-8b-chat-hf",
    "Meta Llama 3.1 70B Instruct Turbo": "albert/meta-llama-3-1-70b-instruct-turbo",
    "Meta Llama 3.1 8B Instruct Turbo": "atlas/llama-3-1-8b-instruct-turbo",
    "WizardLM-2 (8x22B)": "microsoft/WizardLM-2-8x22B",
    "Mixtral-8x7B Instruct v0.1": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "Meta Llama 3.1 405B Instruct Turbo": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    "Meta Llama 3 70B Instruct Reference": "meta-llama/Llama-3-70b-chat-hf",
    "DBRX Instruct": "databricks/dbrx-instruct",
    "Nous Hermes 2 - Mixtral 8x7B-DPO ": "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    "Meta Llama 3 8B Instruct Turbo": "meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
    "Meta Llama 3 8B Instruct Lite": "meta-llama/Meta-Llama-3-8B-Instruct-Lite",
    "Meta Llama 3.1 8B Instruct": "meta-llama/Meta-Llama-3.1-8B-Instruct-Reference",
    "Mixtral-8x22B Instruct v0.1": "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "Gryphe MythoMax L2 Lite (13B)": "Gryphe/MythoMax-L2-13b-Lite",
    "Hermes 3 - Llama-3.1 405B": "NousResearch/Hermes-3-Llama-3.1-405B-Turbo",
    "LLaMA-2 Chat (7B)": "togethercomputer/llama-2-7b-chat",
    "LLaVa-Next (Mistral-7B)": "llava-hf/llava-v1.6-mistral-7b-hf",
    "WizardLM v1.2 (13B)": "WizardLM/WizardLM-13B-V1.2",
    "Koala (7B)": "togethercomputer/Koala-7B",
    "Qwen 2 Instruct (1.5B)": "Qwen/Qwen2-1.5B-Instruct",
    "OpenHermes-2-Mistral (7B)": "teknium/OpenHermes-2-Mistral-7B",
    "Qwen 2 Instruct (7B)": "Qwen/Qwen2-7B-Instruct",
    "Guanaco (65B) ": "togethercomputer/guanaco-65b",
    "ReMM SLERP L2 (13B)": "Undi95/ReMM-SLERP-L2-13B",
    "Vicuna v1.3 (7B)": "lmsys/vicuna-7b-v1.3",
    "Toppy M (7B)": "Undi95/Toppy-M-7B",
    "Nous Hermes LLaMA-2 (70B)": "NousResearch/Nous-Hermes-Llama2-70b",
    "Vicuna v1.5 16K (13B)": "lmsys/vicuna-13b-v1.5-16k",
    "OpenChat 3.5": "openchat/openchat-3.5-1210",
    "Zephyr-7B-ß": "HuggingFaceH4/zephyr-7b-beta",
    "Chronos Hermes (13B)": "Austism/chronos-hermes-13b",
    "Snorkel Mistral PairRM DPO (7B)": "snorkelai/Snorkel-Mistral-PairRM-DPO",
    "Qwen 1.5 Chat (14B)": "Qwen/Qwen1.5-14B-Chat",
    "Qwen 1.5 Chat (1.8B)": "Qwen/Qwen1.5-1.8B-Chat",
    "Snowflake Arctic Instruct": "Snowflake/snowflake-arctic-instruct",
    "Nous Hermes 2 - Mixtral 8x7B-SFT": "NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT",
    "Deepseek Coder Instruct (33B)": "deepseek-ai/deepseek-coder-33b-instruct",
    "Code Llama Instruct (7B)": "codellama/CodeLlama-7b-Instruct-hf",
    "Nous Hermes Llama-2 (13B)": "NousResearch/Nous-Hermes-Llama2-13b",
    "Vicuna v1.5 (13B)": "lmsys/vicuna-13b-v1.5",
    "Guanaco (13B) ": "togethercomputer/guanaco-13b",
    "Code Llama Instruct (13B)": "togethercomputer/CodeLlama-13b-Instruct",
    "Vicuna v1.3 (13B)": "lmsys/vicuna-13b-v1.3",
    "Nous Hermes 2 - Mistral DPO (7B)": "NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
    "Alpaca (7B)": "togethercomputer/alpaca-7b",
    "Platypus2 Instruct (70B)": "garage-bAInd/Platypus2-70B-instruct",
    "Gemma Instruct (7B)": "google/gemma-7b-it",
    "OLMo Instruct (7B)": "allenai/OLMo-7B-Instruct",
    "Guanaco (33B) ": "togethercomputer/guanaco-33b",
    "Koala (13B)": "togethercomputer/Koala-13B",
    "Upstage SOLAR Instruct v1 (11B)-Int4": "togethercomputer/SOLAR-10.7B-Instruct-v1.0-int4",
    "Guanaco (7B) ": "togethercomputer/guanaco-7b",
    "OpenOrca Mistral (7B) 8K": "Open-Orca/Mistral-7B-OpenOrca",
    "Nous Hermes LLaMA-2 (7B)": "NousResearch/Nous-Hermes-llama-2-7b",
    "Qwen 1.5 Chat (32B)": "Qwen/Qwen1.5-32B-Chat",
    "Nous Capybara v1.9 (7B)": "NousResearch/Nous-Capybara-7B-V1p9",
    "Meta Llama 3 8B Instruct": "meta-llama/Meta-Llama-3-8B-Instruct",
    "Vicuna v1.5 (7B)": "lmsys/vicuna-7b-v1.5",
    "01-ai Yi Chat (34B)": "zero-one-ai/Yi-34B-Chat",
    "Meta Llama 3 70B Instruct": "meta-llama/Meta-Llama-3-70B-Instruct",
    "Code Llama Instruct (70B)": "codellama/CodeLlama-70b-Instruct-hf",
    "Hermes 2 Theta Llama-3 70B": "NousResearch/Hermes-2-Theta-Llama-3-70B",
    "Qwen 1.5 Chat (7B)": "Qwen/Qwen1.5-7B-Chat",
    "Dolphin 2.5 Mixtral 8x7b": "cognitivecomputations/dolphin-2.5-mixtral-8x7b",
    "LLaMA-2 Chat (70B)": "meta-llama/Llama-2-70b-chat-hf",
    "Qwen 1.5 Chat (0.5B)": "Qwen/Qwen1.5-0.5B-Chat",
    "OpenHermes-2.5-Mistral (7B)": "teknium/OpenHermes-2p5-Mistral-7B",
    "Qwen 1.5 Chat (4B)": "Qwen/Qwen1.5-4B-Chat",
    "carson ml318br": "carson/ml318br",
    "Llama-3 70B Instruct Gradient 1048K": "gradientai/Llama-3-70B-Instruct-Gradient-1048k",
    "Meta Llama 3.1 70B Instruct": "meta-llama/Meta-Llama-3.1-70B-Instruct-Reference",
}

TogetherModels: TypeAlias = Literal[tuple(together_model_string.keys())]  # type: ignore[valid-type]


@register("secret")
class TogetherAIAPIKey(Model):
    api_key: Annotated[
        str,
        Field(
            title="API Key",
            description="The API Key from Together AI",
            tooltip_message="The API key specified here will be used to authenticate requests to Together AI services.",
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
        Field(
            description="The model to use for the Together API",
            tooltip_message="Choose the model that the LLM uses to interact with Together AI services.",
        ),
    ] = "Meta Llama 3 70B Instruct Reference"

    api_key: Annotated[
        TogetherAIAPIKeyRef,
        Field(
            title="API Key",
            description="The API Key from Together.ai",
            tooltip_message="Choose the API key that will be used to authenticate requests to Together AI services.",
        ),
    ]

    base_url: Annotated[
        URL,
        Field(
            title="Base URL",
            description="The base URL of the OpenAI API",
            tooltip_message="The base URL that the LLM uses to interact with Together AI services.",
        ),
    ] = URL(url="https://api.together.xyz/v1")

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
            tooltip_message="Adjust the temperature to change the response style. Lower values lead to more consistent answers, while higher values make the responses more creative. The values must be between 0 and 2.",
            ge=0.0,
            le=2.0,
        ),
    ] = 0.8

    @classmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> dict[str, Any]:
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
