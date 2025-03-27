from typing import Annotated, Any, Optional

import pytest
from autogen.agentchat import ConversableAgent
from fastapi import FastAPI


def create_app_with_two_enpoints_same_datamodel(host: str, port: str) -> FastAPI:
    app = FastAPI(
        title="test",
        servers=[
            {"url": f"http://{host}:{port}", "description": "Local development server"}
        ],
    )

    @app.get("/get-sheet", description="Get data from a Google Sheet")
    async def get_sheet(
        spreadsheet_id: Annotated[
            Optional[str], "ID of the Google Sheet to fetch data from"
        ] = None,
    ) -> str:
        return "sheet retrieved"

    @app.post(
        "/update-sheet",
        description="Update data in a Google Sheet within the existing spreadsheet",
    )
    async def update_sheet(
        spreadsheet_id: Annotated[
            Optional[str], "ID of the Google Sheet to fetch data from"
        ] = None,
    ) -> str:
        return "Updated"

    return app


@pytest.mark.skip(reason="fastagency.api.openapi.OpenAPI is not implemented yet.")
@pytest.mark.parametrize(
    "fastapi_openapi_url",
    [(create_app_with_two_enpoints_same_datamodel)],
    indirect=["fastapi_openapi_url"],
)
def test_openapi_same_schema_in_parameters_register_for_llm(
    fastapi_openapi_url: str,
    azure_gpt35_turbo_16k_llm_config: dict[str, Any],
) -> None:
    from fastagency.api.openapi import OpenAPI

    api_client = OpenAPI.create(
        openapi_url=fastapi_openapi_url,
    )
    agent = ConversableAgent(name="agent", llm_config=azure_gpt35_turbo_16k_llm_config)
    api_client._register_for_llm(agent)
    tools = agent.llm_config["tools"]

    expected = [
        {
            "type": "function",
            "function": {
                "description": "Get data from a Google Sheet",
                "name": "get_sheet_get_sheet_get",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spreadsheet_id": {
                            "$defs": {
                                "SpreadsheetId": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "SpreadsheetId",
                                }
                            },
                            "anyOf": [
                                {"$ref": "#/$defs/SpreadsheetId"},
                                {"type": "null"},
                            ],
                            "default": None,
                            "description": "spreadsheet_id",
                        }
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "description": "Update data in a Google Sheet within the existing spreadsheet",
                "name": "update_sheet_update_sheet_post",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spreadsheet_id": {
                            "$defs": {
                                "SpreadsheetId": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "SpreadsheetId",
                                }
                            },
                            "anyOf": [
                                {"$ref": "#/$defs/SpreadsheetId"},
                                {"type": "null"},
                            ],
                            "default": None,
                            "description": "spreadsheet_id",
                        }
                    },
                    "required": [],
                },
            },
        },
    ]

    assert tools == expected, tools
