import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Any, Dict, Iterator, Optional

import fastapi
import pytest
from autogen.agentchat import ConversableAgent
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel, Field

from fastagency.openapi.client import Client


class TestClientEnd2End:
    @pytest.fixture()
    def fastapi_app(self) -> FastAPI:
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

        class Item(BaseModel):
            name: Annotated[str, Field(description="The name of the item")]
            description: Annotated[
                Optional[str], Field(description="The description of the item")
            ] = None
            price: float
            tax: Optional[float] = None

        @app.get("/items/{item_id}", description="Read an item by ID")
        async def read_item(
            item_id: Annotated[
                int, fastapi.Path(description="The ID of the item to get")
            ],
            q: Annotated[
                Optional[str], Query(description="some extra query parameter")
            ] = None,
        ) -> Dict[str, Any]:
            return {"item_id": item_id, "q": q}

        @app.post("/items/")
        async def create_item(
            item: Annotated[Item, Body(description="The item to create")],
        ) -> Dict[str, Any]:
            item_id = 1
            return {"item_id": item_id, "item": item}

        @app.put("/items/{item_id}", description="Update an item by ID")
        async def update_item(
            item_id: Annotated[
                int, fastapi.Path(description="The ID of the item to update")
            ],
            item: Annotated[Item, Body(description="The item to update")],
        ) -> Dict[str, Any]:
            return {"item_id": item_id, "item": item}

        @app.delete("/items/{item_id}", description="Delete an item by ID")
        async def delete_item(
            item_id: Annotated[
                int, fastapi.Path(description="The ID of the item to delete")
            ],
        ) -> Dict[str, Any]:
            return {"item_id": item_id}

        return app

    def test_openapi_app(self, fastapi_app: FastAPI) -> None:
        assert fastapi_app is not None
        assert isinstance(fastapi_app, FastAPI)

    @pytest.fixture()
    def openapi_schema(self, fastapi_app: FastAPI) -> Dict[str, Any]:
        return fastapi_app.openapi()

    def test_openapi_schema(self, openapi_schema: Dict[str, Any]) -> None:
        expected = {
            "openapi": "3.1.0",
            "info": {
                "title": "My FastAPI app",
                "description": "Test FastAPI app to check OpenAPI schema generation.",
                "version": "0.1.0",
            },
            "servers": [
                {
                    "url": "https://stag.example.com",
                    "description": "Staging environment",
                },
                {
                    "url": "https://prod.example.com",
                    "description": "Production environment",
                },
            ],
            "paths": {
                "/items/{item_id}": {
                    "get": {
                        "summary": "Read Item",
                        "operationId": "read_item_items__item_id__get",
                        "description": "Read an item by ID",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer",
                                    "description": "The ID of the item to get",
                                    "title": "Item Id",
                                },
                                "description": "The ID of the item to get",
                            },
                            {
                                "name": "q",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "description": "some extra query parameter",
                                    "title": "Q",
                                },
                                "description": "some extra query parameter",
                            },
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "title": "Response Read Item Items  Item Id  Get",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    },
                    "put": {
                        "summary": "Update Item",
                        "operationId": "update_item_items__item_id__put",
                        "description": "Update an item by ID",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer",
                                    "description": "The ID of the item to update",
                                    "title": "Item Id",
                                },
                                "description": "The ID of the item to update",
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "description": "The item to update",
                                        "title": "Item",
                                    }
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "title": "Response Update Item Items  Item Id  Put",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    },
                    "delete": {
                        "summary": "Delete Item",
                        "operationId": "delete_item_items__item_id__delete",
                        "description": "Delete an item by ID",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer",
                                    "description": "The ID of the item to delete",
                                    "title": "Item Id",
                                },
                                "description": "The ID of the item to delete",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "title": "Response Delete Item Items  Item Id  Delete",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    },
                },
                "/items/": {
                    "post": {
                        "summary": "Create Item",
                        "operationId": "create_item_items__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Item",
                                        "description": "The item to create",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "title": "Response Create Item Items  Post",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "Item": {
                        "properties": {
                            "name": {
                                "type": "string",
                                "title": "Name",
                                "description": "The name of the item",
                            },
                            "description": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Description",
                                "description": "The description of the item",
                            },
                            "price": {"type": "number", "title": "Price"},
                            "tax": {
                                "anyOf": [{"type": "number"}, {"type": "null"}],
                                "title": "Tax",
                            },
                        },
                        "type": "object",
                        "required": ["name", "price"],
                        "title": "Item",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
        assert openapi_schema == expected

    @pytest.fixture()
    def generated_code_path(self, openapi_schema: Dict[str, Any]) -> Iterator[Path]:
        with TemporaryDirectory() as temp_dir:
            td = Path(temp_dir)
            Client.generate_code(
                json.dumps(openapi_schema), output_dir=td, disable_timestamp=True
            )
            yield td

    def test_generated_code_main(self, generated_code_path: Path) -> None:
        expected = '''# generated by fastapi-codegen:
#   filename:  openapi.json

from __future__ import annotations

from typing import *
from typing import Optional, Union

from fastagency.openapi.client import Client

from models_tmp61z6vu75 import (
    HTTPValidationError,
    ItemsItemIdDeleteResponse,
    ItemsItemIdGetResponse,
    ItemsItemIdPutRequest,
    ItemsItemIdPutResponse,
    ItemsPostRequest,
    ItemsPostResponse,
)

app = Client(
    title='My FastAPI app',
    description='Test FastAPI app to check OpenAPI schema generation.',
    version='0.1.0',
    servers=[
        {'url': 'https://stag.example.com', 'description': 'Staging environment'},
        {'url': 'https://prod.example.com', 'description': 'Production environment'},
    ],
)


@app.post(
    '/items/',
    response_model=ItemsPostResponse,
    responses={'422': {'model': HTTPValidationError}},
)
def create_item_items__post(
    body: ItemsPostRequest,
) -> Union[ItemsPostResponse, HTTPValidationError]:
    """
    Create Item
    """
    pass


@app.get(
    '/items/{item_id}',
    response_model=ItemsItemIdGetResponse,
    description="Read an item by ID",
    responses={'422': {'model': HTTPValidationError}},
)
def read_item_items__item_id__get(
    item_id: Annotated[int, """The ID of the item to get"""],
    q: Annotated[Optional[str], """some extra query parameter"""] = None,
) -> Union[ItemsItemIdGetResponse, HTTPValidationError]:
    """
    Read Item
    """
    pass


@app.put(
    '/items/{item_id}',
    response_model=ItemsItemIdPutResponse,
    description="Update an item by ID",
    responses={'422': {'model': HTTPValidationError}},
)
def update_item_items__item_id__put(
    item_id: Annotated[int, """The ID of the item to update"""],
    body: ItemsItemIdPutRequest = ...,
) -> Union[ItemsItemIdPutResponse, HTTPValidationError]:
    """
    Update Item
    """
    pass


@app.delete(
    '/items/{item_id}',
    response_model=ItemsItemIdDeleteResponse,
    description="Delete an item by ID",
    responses={'422': {'model': HTTPValidationError}},
)
def delete_item_items__item_id__delete(
    item_id: Annotated[int, """The ID of the item to delete"""]
) -> Union[ItemsItemIdDeleteResponse, HTTPValidationError]:
    """
    Delete Item
    """
    pass
'''
        sufix = generated_code_path.name
        expected = expected.replace("tmp61z6vu75", sufix)

        assert generated_code_path.exists()
        assert generated_code_path.is_dir()

        path = generated_code_path / f"main_{sufix}.py"
        assert path.exists()

        with path.open() as f:
            main = f.read()
            assert main == expected

    def test_generated_code_models(self, generated_code_path: Path) -> None:
        expected = """# generated by fastapi-codegen:
#   filename:  openapi.json

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(..., description='The name of the item', title='Name')
    description: Optional[str] = Field(
        None, description='The description of the item', title='Description'
    )
    price: float = Field(..., title='Price')
    tax: Optional[float] = Field(None, title='Tax')


class ValidationError(BaseModel):
    loc: List[Union[str, int]] = Field(..., title='Location')
    msg: str = Field(..., title='Message')
    type: str = Field(..., title='Error Type')


class ItemsItemIdGetResponse(BaseModel):
    pass


class ItemsItemIdPutRequest(Item):
    pass


class ItemsItemIdPutResponse(BaseModel):
    pass


class ItemsItemIdDeleteResponse(BaseModel):
    pass


class ItemsPostRequest(Item):
    pass


class ItemsPostResponse(BaseModel):
    pass


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title='Detail')
"""
        assert generated_code_path.exists()
        assert generated_code_path.is_dir()
        sufix = generated_code_path.name

        path = generated_code_path / f"models_{sufix}.py"
        assert path.exists()

        with path.open() as f:
            models = f.read()
            assert models == expected

    @pytest.fixture()
    def client(self, openapi_schema: Dict[str, Any]) -> Client:
        client = Client.create(json.dumps(openapi_schema))
        return client

    def test_client(self, client: Client) -> None:
        assert client is not None
        assert isinstance(client, Client)

        assert len(client.registered_funcs) == 4, client.registered_funcs

        expected_func_desc = {
            "create_item_items__post": "Create Item",
            "read_item_items__item_id__get": "Read an item by ID",
            "update_item_items__item_id__put": "Update an item by ID",
            "delete_item_items__item_id__delete": "Delete an item by ID",
        }
        func_desc = {
            func.__name__: func._description  # type: ignore[attr-defined]
            for func in client.registered_funcs
        }
        assert func_desc == expected_func_desc

    def test_register_for_llm(
        self, client: Client, azure_gpt35_turbo_16k_llm_config: Dict[str, Any]
    ) -> None:
        expected_tools = [
            {
                "type": "function",
                "function": {
                    "description": "Create Item",
                    "name": "create_item_items__post",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "body": {
                                "properties": {
                                    "name": {
                                        "description": "The name of the item",
                                        "title": "Name",
                                        "type": "string",
                                    },
                                    "description": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "default": None,
                                        "description": "The description of the item",
                                        "title": "Description",
                                    },
                                    "price": {"title": "Price", "type": "number"},
                                    "tax": {
                                        "anyOf": [{"type": "number"}, {"type": "null"}],
                                        "default": None,
                                        "title": "Tax",
                                    },
                                },
                                "required": ["name", "price"],
                                "title": "ItemsPostRequest",
                                "type": "object",
                                "description": "body",
                            }
                        },
                        "required": ["body"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "description": "Read an item by ID",
                    "name": "read_item_items__item_id__get",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_id": {
                                "type": "integer",
                                "description": "The ID of the item to get",
                            },
                            "q": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": "some extra query parameter",
                            },
                        },
                        "required": ["item_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "description": "Update an item by ID",
                    "name": "update_item_items__item_id__put",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_id": {
                                "type": "integer",
                                "description": "The ID of the item to update",
                            },
                            "body": {
                                "properties": {
                                    "name": {
                                        "description": "The name of the item",
                                        "title": "Name",
                                        "type": "string",
                                    },
                                    "description": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "default": None,
                                        "description": "The description of the item",
                                        "title": "Description",
                                    },
                                    "price": {"title": "Price", "type": "number"},
                                    "tax": {
                                        "anyOf": [{"type": "number"}, {"type": "null"}],
                                        "default": None,
                                        "title": "Tax",
                                    },
                                },
                                "required": ["name", "price"],
                                "title": "ItemsItemIdPutRequest",
                                "type": "object",
                                "default": Ellipsis,
                                "description": "body",
                            },
                        },
                        "required": ["item_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "description": "Delete an item by ID",
                    "name": "delete_item_items__item_id__delete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_id": {
                                "type": "integer",
                                "description": "The ID of the item to delete",
                            }
                        },
                        "required": ["item_id"],
                    },
                },
            },
        ]

        agent = ConversableAgent(
            name="agent", llm_config=azure_gpt35_turbo_16k_llm_config
        )
        client.register_for_llm(agent)
        tools = agent.llm_config["tools"]

        assert tools == expected_tools

    def test_register_for_execution(
        self, client: Client, azure_gpt35_turbo_16k_llm_config: Dict[str, Any]
    ) -> None:
        expected_keys = {
            "create_item_items__post",
            "read_item_items__item_id__get",
            "update_item_items__item_id__put",
            "delete_item_items__item_id__delete",
        }
        agent = ConversableAgent(
            name="agent", llm_config=azure_gpt35_turbo_16k_llm_config
        )
        client.register_for_execution(agent)
        function_map = agent.function_map

        assert set(function_map.keys()) == expected_keys
