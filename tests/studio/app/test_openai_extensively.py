import json
import uuid
from typing import Any, Dict

import pytest
from fastapi import BackgroundTasks, HTTPException
from fastapi.testclient import TestClient

from fastagency.studio.app import add_model, app, validate_toolbox
from fastagency.studio.models.llms.openai import OpenAI, OpenAIAPIKey
from fastagency.studio.models.registry import Schemas
from fastagency.studio.models.toolboxes.toolbox import OpenAPIAuth, Toolbox

client = TestClient(app)


class TestValidateOpenAIKey:
    @pytest.fixture
    def model_dict(self) -> Dict[str, Any]:
        model = OpenAIAPIKey(
            api_key="sk-sUeBP9asw6GiYHXqtg70T3BlbkFJJuLwJFco90bOpU0Ntest",  # pragma: allowlist secret
            name="Hello World!",
        )

        return json.loads(model.model_dump_json())  # type: ignore[no-any-return]

    def test_validate_success(self, model_dict: Dict[str, Any]) -> None:
        response = client.post(
            "/models/secret/OpenAIAPIKey/validate",
            json=model_dict,
        )
        assert response.status_code == 200

    def test_validate_incorrect_api_key(self, model_dict: Dict[str, Any]) -> None:
        model_dict["api_key"] = "whatever"  # pragma: allowlist secret

        response = client.post(
            "/models/secret/OpenAIAPIKey/validate",
            json=model_dict,
        )
        assert response.status_code == 422
        msg_dict = response.json()["detail"][0]
        msg_dict.pop("input")
        msg_dict.pop("url")
        expected = {
            "type": "value_error",
            "loc": ["api_key"],
            "msg": "Value error, Invalid OpenAI API Key",
            "ctx": {"error": "Invalid OpenAI API Key"},
        }
        assert msg_dict == expected

    @pytest.mark.db
    @pytest.mark.asyncio
    async def test_validate_secret_model(
        self,
        model_dict: Dict[str, Any],
        user_uuid: str,
    ) -> None:
        api_key = OpenAIAPIKey(**model_dict)
        api_key_model_uuid = str(uuid.uuid4())
        await add_model(
            user_uuid=user_uuid,
            type_name="secret",
            model_name=OpenAIAPIKey.__name__,  # type: ignore [attr-defined]
            model_uuid=api_key_model_uuid,
            model=api_key.model_dump(),
            background_tasks=BackgroundTasks(),
        )

        # Remove api_key and send name alone to validate route
        model_dict.pop("api_key")

        response = client.post(
            f"/user/{user_uuid}/models/secret/OpenAIAPIKey/{api_key_model_uuid}/validate",
            json=model_dict,
        )
        assert response.status_code == 200


# we will do this for OpenAI only, the rest should be the same
class TestValidateOpenAI:
    @pytest.fixture
    def model_dict(self) -> Dict[str, Any]:
        key_uuid = uuid.uuid4()
        OpenAIAPIKeyRef = OpenAIAPIKey.get_reference_model()  # noqa: N806
        api_key = OpenAIAPIKeyRef(uuid=key_uuid)

        model = OpenAI(api_key=api_key, name="Hello World!")

        return json.loads(model.model_dump_json())  # type: ignore[no-any-return]

    def test_get_openai_schema(self) -> None:
        response = client.get("/models/schemas")
        assert response.status_code == 200

        schemas = Schemas(**response.json())
        llm_schema = next(
            schemas for schemas in schemas.list_of_schemas if schemas.name == "llm"
        )

        openai_schema = next(
            schema for schema in llm_schema.schemas if schema.name == OpenAI.__name__
        )

        assert len(openai_schema.json_schema) > 0

    def test_validate_success(self, model_dict: Dict[str, Any]) -> None:
        response = client.post(
            "/models/llm/OpenAI/validate",
            json=model_dict,
        )
        assert response.status_code == 200

    def test_validate_missing_key(self, model_dict: Dict[str, Any]) -> None:
        model_dict.pop("api_key")

        response = client.post(
            "/models/llm/OpenAI/validate",
            json=model_dict,
        )
        assert response.status_code == 422
        msg_dict = response.json()["detail"][0]
        msg_dict.pop("input")
        msg_dict.pop("url")
        expected = {
            "type": "missing",
            "loc": ["api_key"],
            "msg": "Field required",
        }
        assert msg_dict == expected

    def test_validate_incorrect_model(self, model_dict: Dict[str, Any]) -> None:
        model_dict["model"] = model_dict["model"] + "_turbo_diezel"

        response = client.post(
            "/models/llm/OpenAI/validate",
            json=model_dict,
        )
        assert response.status_code == 422
        msg_dict = response.json()["detail"][0]
        msg_dict.pop("input")
        msg_dict.pop("url")
        expected = {
            "type": "literal_error",
            "loc": ["model"],
            "msg": "Input should be 'gpt-4o-2024-08-06', 'gpt-4-1106-preview', 'gpt-4-0613', 'gpt-4', 'chatgpt-4o-latest', 'gpt-4-turbo-preview', 'gpt-4-0125-preview', 'gpt-3.5-turbo', 'gpt-3.5-turbo-1106', 'gpt-4o-mini-2024-07-18', 'gpt-3.5-turbo-0125', 'gpt-4o-mini', 'gpt-3.5-turbo-16k', 'gpt-4-turbo-2024-04-09', 'gpt-3.5-turbo-instruct-0914', 'gpt-3.5-turbo-instruct', 'gpt-4o', 'gpt-4o-2024-05-13' or 'gpt-4-turbo'",
            "ctx": {
                "expected": "'gpt-4o-2024-08-06', 'gpt-4-1106-preview', 'gpt-4-0613', 'gpt-4', 'chatgpt-4o-latest', 'gpt-4-turbo-preview', 'gpt-4-0125-preview', 'gpt-3.5-turbo', 'gpt-3.5-turbo-1106', 'gpt-4o-mini-2024-07-18', 'gpt-3.5-turbo-0125', 'gpt-4o-mini', 'gpt-3.5-turbo-16k', 'gpt-4-turbo-2024-04-09', 'gpt-3.5-turbo-instruct-0914', 'gpt-3.5-turbo-instruct', 'gpt-4o', 'gpt-4o-2024-05-13' or 'gpt-4-turbo'"
            },
        }
        # print(f"{msg_dict=}")
        assert msg_dict == expected

    def test_validate_incorrect_base_url(self, model_dict: Dict[str, Any]) -> None:
        model_dict["base_url"] = "mailto://api.openai.com/v1"

        response = client.post(
            "/models/llm/OpenAI/validate",
            json=model_dict,
        )
        assert response.status_code == 422
        msg_dict = response.json()["detail"][0]
        msg_dict.pop("input")
        msg_dict.pop("url")
        expected = {
            "ctx": {"expected_schemes": "'http' or 'https'"},
            "loc": ["base_url"],
            "msg": "URL scheme should be 'http' or 'https'",
            "type": "url_scheme",
        }
        assert msg_dict == expected


def test_get_schemas() -> None:
    response = client.get("/models/schemas")
    assert response.status_code == 200

    schemas = Schemas(**response.json())
    assert len(schemas.list_of_schemas) >= 2


class TestToolbox:
    @pytest.mark.db
    @pytest.mark.asyncio
    async def test_add_toolbox(self, user_uuid: str, fastapi_openapi_url: str) -> None:
        openapi_auth = OpenAPIAuth(
            name="openapi_auth_secret",
            username="test",
            password="password",  # pragma: allowlist secret
        )
        openapi_auth_model_uuid = str(uuid.uuid4())
        response = client.post(
            f"/user/{user_uuid}/models/secret/OpenAPIAuth/{openapi_auth_model_uuid}",
            json=openapi_auth.model_dump(),
        )
        assert response.status_code == 200

        model_uuid = str(uuid.uuid4())
        toolbox = Toolbox(
            name="test_toolbox_constructor",
            openapi_url=fastapi_openapi_url,
            openapi_auth=openapi_auth.get_reference_model()(
                uuid=openapi_auth_model_uuid
            ),
        )
        toolbox_dump = toolbox.model_dump()
        toolbox_dump["openapi_auth"]["uuid"] = str(toolbox_dump["openapi_auth"]["uuid"])

        response = client.post(
            f"/user/{user_uuid}/models/toolbox/Toolbox/{model_uuid}",
            json=toolbox_dump,
        )

        assert response.status_code == 200
        expected = {
            "name": "test_toolbox_constructor",
            "openapi_url": fastapi_openapi_url,
            "openapi_auth": {
                "type": "secret",
                "name": "OpenAPIAuth",
                "uuid": str(openapi_auth_model_uuid),
            },
        }
        actual = response.json()
        assert actual == expected

    @pytest.mark.asyncio
    async def test_validate_toolbox(self, fastapi_openapi_url: str) -> None:
        openapi_auth = OpenAPIAuth(
            name="openapi_auth_secret",
            username="test",
            password="password",  # pragma: allowlist secret
        )
        openapi_auth_model_uuid = str(uuid.uuid4())

        toolbox = Toolbox(
            name="test_toolbox_constructor",
            openapi_url=fastapi_openapi_url,
            openapi_auth=openapi_auth.get_reference_model()(
                uuid=openapi_auth_model_uuid
            ),
        )

        await validate_toolbox(toolbox)

    @pytest.mark.asyncio
    async def test_validate_toolbox_route(self, fastapi_openapi_url: str) -> None:
        openapi_auth = OpenAPIAuth(
            name="openapi_auth_secret",
            username="test",
            password="password",  # pragma: allowlist secret
        )
        openapi_auth_model_uuid = str(uuid.uuid4())

        toolbox = Toolbox(
            name="test_toolbox_constructor",
            openapi_url=fastapi_openapi_url,
            openapi_auth=openapi_auth.get_reference_model()(
                uuid=openapi_auth_model_uuid
            ),
        )
        toolbox_dump = toolbox.model_dump()
        toolbox_dump["openapi_auth"]["uuid"] = str(toolbox_dump["openapi_auth"]["uuid"])

        response = client.post(
            "/models/toolbox/Toolbox/validate",
            json=toolbox_dump,
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_validate_toolbox_with_404_url(self) -> None:
        invalid_url = "http://i.dont.exist.airt.ai/openapi.json"

        openapi_auth = OpenAPIAuth(
            name="openapi_auth_secret",
            username="test",
            password="password",  # pragma: allowlist secret
        )
        openapi_auth_model_uuid = str(uuid.uuid4())

        toolbox = Toolbox(
            name="test_toolbox_constructor",
            openapi_url=invalid_url,
            openapi_auth=openapi_auth.get_reference_model()(
                uuid=openapi_auth_model_uuid
            ),
        )

        with pytest.raises(HTTPException) as e:
            await validate_toolbox(toolbox)

        assert e.value.status_code == 422
        assert e.value.detail == "OpenAPI URL is invalid"

    @pytest.mark.asyncio
    async def test_validate_toolbox_with_invalid_openapi_spec(self) -> None:
        invalid_url = "http://echo.jsontest.com/key/value/one/two"

        openapi_auth = OpenAPIAuth(
            name="openapi_auth_secret",
            username="test",
            password="password",  # pragma: allowlist secret
        )
        openapi_auth_model_uuid = str(uuid.uuid4())

        toolbox = Toolbox(
            name="test_toolbox_constructor",
            openapi_url=invalid_url,
            openapi_auth=openapi_auth.get_reference_model()(
                uuid=openapi_auth_model_uuid
            ),
        )

        with pytest.raises(HTTPException) as e:
            await validate_toolbox(toolbox)

        assert e.value.status_code == 422
        assert e.value.detail == "OpenAPI URL does not contain a valid OpenAPI spec"

    @pytest.mark.asyncio
    async def test_validate_toolbox_with_yaml_openapi_spec(self) -> None:
        invalid_url = "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.yaml"

        openapi_auth = OpenAPIAuth(
            name="openapi_auth_secret",
            username="test",
            password="password",  # pragma: allowlist secret
        )
        openapi_auth_model_uuid = str(uuid.uuid4())

        toolbox = Toolbox(
            name="test_toolbox_constructor",
            openapi_url=invalid_url,
            openapi_auth=openapi_auth.get_reference_model()(
                uuid=openapi_auth_model_uuid
            ),
        )

        await validate_toolbox(toolbox)
