from typing import Any, Dict

import httpx
import pytest

from fastagency.helpers import get_model_by_ref
from fastagency.models.base import ObjectReference

from .conftest import find_free_port


def test_azure_gpt35_turbo_16k_llm_config(
    azure_gpt35_turbo_16k_llm_config: Dict[str, Any],
) -> None:
    assert set(azure_gpt35_turbo_16k_llm_config.keys()) == {
        "config_list",
        "temperature",
    }
    assert isinstance(azure_gpt35_turbo_16k_llm_config["config_list"], list)
    assert azure_gpt35_turbo_16k_llm_config["temperature"] == 0.8

    assert (
        azure_gpt35_turbo_16k_llm_config["config_list"][0]["model"]
        == "gpt-35-turbo-16k"
    )

    for k in ["model", "api_key", "base_url", "api_type", "api_version"]:
        assert len(azure_gpt35_turbo_16k_llm_config["config_list"][0][k]) > 3


def test_openai_gpt35_turbo_16k_llm_config(
    openai_gpt35_turbo_16k_llm_config: Dict[str, Any],
) -> None:
    api_key = openai_gpt35_turbo_16k_llm_config["config_list"][0]["api_key"]
    expected = {
        "config_list": [
            {
                "model": "gpt-3.5-turbo",
                "api_key": api_key,  # pragma: allowlist secret
            }
        ],
        "temperature": 0.8,
    }
    assert openai_gpt35_turbo_16k_llm_config == expected


@pytest.mark.db()
@pytest.mark.asyncio()
async def test_azure_oai_key_ref(azure_oai_key_ref: ObjectReference) -> None:
    assert isinstance(azure_oai_key_ref, ObjectReference)
    assert azure_oai_key_ref.type == "secret"
    assert azure_oai_key_ref.name == "AzureOAIAPIKey"

    azure_oai_key = await get_model_by_ref(azure_oai_key_ref)
    assert azure_oai_key.name.startswith("azure_oai_key_")


@pytest.mark.db()
@pytest.mark.asyncio()
async def test_azure_oai_gpt35_ref(azure_oai_gpt35_ref: ObjectReference) -> None:
    assert isinstance(azure_oai_gpt35_ref, ObjectReference)
    assert azure_oai_gpt35_ref.type == "llm"
    assert azure_oai_gpt35_ref.name == "AzureOAI"

    azure_oai_key = await get_model_by_ref(azure_oai_gpt35_ref)
    assert azure_oai_key.name.startswith("azure_oai_")


def test_find_free_port() -> None:
    port = find_free_port()
    assert isinstance(port, int)
    assert 1024 <= port <= 65535


def test_fastapi_openapi(fastapi_openapi_url: str) -> None:
    assert isinstance(fastapi_openapi_url, str)

    resp = httpx.get(fastapi_openapi_url)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert "openapi" in resp_json
    assert "servers" in resp_json
    assert len(resp_json["servers"]) == 1
    assert resp_json["info"]["title"] == "FastAPI"


def test_weather_fastapi_openapi(weather_fastapi_openapi_url: str) -> None:
    assert isinstance(weather_fastapi_openapi_url, str)

    resp = httpx.get(weather_fastapi_openapi_url)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert "openapi" in resp_json
    assert "servers" in resp_json
    assert len(resp_json["servers"]) == 1
    assert resp_json["info"]["title"] == "Weather"


@pytest.mark.db()
@pytest.mark.asyncio()
async def test_weather_toolbox_ref(weather_toolbox_ref: ObjectReference) -> None:
    assert isinstance(weather_toolbox_ref, ObjectReference)


@pytest.mark.anthropic()
def test_empty_anthropic() -> None:
    pass


@pytest.mark.openai()
def test_empty_openai() -> None:
    pass
