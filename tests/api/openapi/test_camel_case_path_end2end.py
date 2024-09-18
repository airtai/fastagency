import json
from collections.abc import Iterator
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import fastapi
import pytest
from autogen.agentchat import ConversableAgent
from fastapi import FastAPI
from pydantic import BaseModel

from fastagency.api.openapi import OpenAPI


class OpenAPIEnd2End:
    @pytest.fixture
    def fastapi_app(self) -> FastAPI:  # noqa: PT004
        raise NotImplementedError

    @pytest.fixture
    def openapi_schema(self, fastapi_app: FastAPI) -> dict[str, Any]:
        return fastapi_app.openapi()

    @pytest.fixture
    def generated_code_path(self, openapi_schema: dict[str, Any]) -> Iterator[Path]:
        with TemporaryDirectory() as temp_dir:
            td = Path(temp_dir)
            OpenAPI.generate_code(
                json.dumps(openapi_schema), output_dir=td, disable_timestamp=True
            )
            yield td

    def _test_generated_code_main_helper(
        self,
        generated_code_path: Path,
        pydantic_version: float,
        expected_pydantic_v28: str,
        expected_pydantic_v29: str,
    ) -> None:
        if pydantic_version >= 2.9:
            # TODO: Add a test for pydantic 2.9 and above
            pytest.skip("Skipped test for pydantic 2.9 and above")

        expected = (
            expected_pydantic_v28 if pydantic_version < 2.9 else expected_pydantic_v29
        )
        suffix = generated_code_path.name

        assert generated_code_path.exists()
        assert generated_code_path.is_dir()

        path = generated_code_path / f"main_{suffix}.py"
        assert path.exists()

        with path.open() as f:
            main = f.read()
            assert expected in main

    @pytest.fixture
    def client(self, openapi_schema: dict[str, Any]) -> OpenAPI:
        client = OpenAPI.create(json.dumps(openapi_schema))
        return client

    # def test_end2end(
    #     self, client: OpenAPI, openai_gpt4o_llm_config: dict[str, Any]
    # ) -> None:
    #     user_agent = UserProxyAgent(
    #         name="User_Agent",
    #         system_message="You are a user agent",
    #         llm_config=openai_gpt4o_llm_config,
    #         human_input_mode="NEVER",
    #     )
    #     api_agent = ConversableAgent(
    #         name="Api_Agent",
    #         system_message="You are an api agent",
    #         llm_config=openai_gpt4o_llm_config,
    #         human_input_mode="NEVER",
    #     )

    #     client._register_for_llm(api_agent)
    #     client._register_for_execution(user_agent)

    #     user_agent.initiate_chat(
    #         api_agent,
    #         message="I need some gif with id 1",
    #         summary_method="reflection_with_llm",
    #         max_turns=3,
    #     )


class TestOpenAPIEnd2EndGiphy(OpenAPIEnd2End):
    @pytest.fixture
    def fastapi_app(self) -> FastAPI:
        class Gif(BaseModel):
            id: str
            title: str
            url: str

        app = FastAPI(
            title="My FastAPI app",
            version="0.1.0",
            description="Test FastAPI app to check OpenAPI schema generation.",
            servers=[
                {
                    "url": "https://stag.example.com",
                    "description": "Staging environment",
                },
                {
                    "url": "https://prod.example.com",
                    "description": "Production environment",
                },
            ],
        )

        @app.get("/gifs/{gifId}", response_model=Gif, tags=["gifs"])
        def get_gif_by_id(gif_id: int = fastapi.Path(alias="gifId")) -> Gif:
            """Get GIF by Id."""
            return Gif(id="1", title="Gif 1", url="https://example.com/gif1")

        return app

    def test_generated_code_main(
        self, generated_code_path: Path, pydantic_version: float
    ) -> None:
        expected_pydantic_v29 = """'TODO: Add a test for pydantic 2.9 and above"""
        expected_pydantic_v28 = '''app = OpenAPI(
    title='My FastAPI app',
    description='Test FastAPI app to check OpenAPI schema generation.',
    version='0.1.0',
    servers=[
        {'url': 'https://stag.example.com', 'description': 'Staging environment'},
        {'url': 'https://prod.example.com', 'description': 'Production environment'},
    ],
)


@app.get(
    '/gifs/{gifId}',
    response_model=Gif,
    description="Get GIF by Id.",
    responses={'422': {'model': HTTPValidationError}},
    tags=['gifs'],
)
def get_gif_by_id_gifs__gif_id__get(
    gif_id: int = Path(..., alias='gifId')
) -> Union[Gif, HTTPValidationError]:
    """
    Get Gif By Id
    """
    pass
'''

        self._test_generated_code_main_helper(
            generated_code_path,
            pydantic_version,
            expected_pydantic_v28,
            expected_pydantic_v29,
        )

    def test_client(self, client: OpenAPI) -> None:
        assert client is not None
        assert isinstance(client, OpenAPI)

        assert len(client.registered_funcs) == 1, client.registered_funcs

        expected_func_desc = {
            "get_gif_by_id_gifs__gif_id__get": "Get GIF by Id.",
        }
        func_desc = {
            func.__name__: func._description  # type: ignore[attr-defined]
            for func in client.registered_funcs
        }
        assert func_desc == expected_func_desc

    def test_register_for_execution(
        self, client: OpenAPI, azure_gpt35_turbo_16k_llm_config: dict[str, Any]
    ) -> None:
        expected_keys = {
            "get_gif_by_id_gifs__gif_id__get",
        }
        agent = ConversableAgent(
            name="agent", llm_config=azure_gpt35_turbo_16k_llm_config
        )
        client._register_for_execution(agent)
        function_map = agent.function_map

        assert set(function_map.keys()) == expected_keys

    def test_register_for_llm(
        self,
        client: OpenAPI,
        azure_gpt35_turbo_16k_llm_config: dict[str, Any],
        pydantic_version: float,
    ) -> None:
        class JSONEncoder(json.JSONEncoder):
            def default(self, o: Any) -> Any:
                if o.__class__.__name__ == "ellipsis":
                    return "Ellipsis"
                return super().default(o)

        if pydantic_version >= 2.9:
            # TODO: Add a test for pydantic 2.9 and above
            pytest.skip("Skipped test for pydantic 2.9 and above")

        expected_tools = [
            {
                "type": "function",
                "function": {
                    "description": "Get GIF by Id.",
                    "name": "get_gif_by_id_gifs__gif_id__get",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "gif_id": {"type": "integer", "description": "gif_id"}
                        },
                        "required": ["gif_id"],
                    },
                },
            }
        ]

        agent = ConversableAgent(
            name="agent", llm_config=azure_gpt35_turbo_16k_llm_config
        )
        client._register_for_llm(agent)
        tools = agent.llm_config["tools"]

        # The problem is in line:
        #     "default": Path(PydanticUndefined),
        # The following is the expected (problematic) output of the tools
        # [
        #     {
        #         "type": "function",
        #         "function": {
        #             "description": "Get GIF by Id.",
        #             "name": "get_gif_by_id_gifs__gif_id__get",
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {
        #                     "gif_id": {
        #                         "type": "integer",
        #                         "default": Path(PydanticUndefined),
        #                         "description": "gif_id",
        #                     }
        #                 },
        #                 "required": [],
        #             },
        #         },
        #     }
        # ]

        # print(tools)

        json_str = json.dumps(tools, cls=JSONEncoder)
        assert json_str == json.dumps(expected_tools, cls=JSONEncoder)
