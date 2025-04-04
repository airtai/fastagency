from typing import Any, Optional, Union

import pytest
import requests
from pydantic import BaseModel, Field

from fastagency.api.openapi import OpenAPI


class Item(BaseModel):
    name: str = Field(..., description="Name of the item", title="Name")
    description: str = Field(
        ..., description="Description of the item", title="Description"
    )
    price: float = Field(..., description="Price of the item", title="Price")
    tax: float = Field(..., description="Tax of the item", title="Tax")


class ValidationError(BaseModel):
    loc: list[Union[str, int]] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")


class HTTPValidationError(BaseModel):
    detail: Optional[list[ValidationError]] = Field(None, title="Detail")


@pytest.fixture
def app() -> OpenAPI:
    return OpenAPI(
        title="FastAPI",
        version="0.1.0",
        servers=[{"url": "http://localhost:8080", "description": "Local environment"}],
    )


class MockResponse:
    def __init__(
        self, json_data: Union[list[dict[str, Any]], dict[str, Any]], status_code: int
    ) -> None:
        """Mock response object for requests."""
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> Union[list[dict[str, Any]], dict[str, Any]]:
        """Return the json data."""
        return self.json_data


def test_process_params_with_query_params_and_path_params(app: OpenAPI) -> None:
    @app.put(
        "/items/{item_id}/ships/{ship}",
        response_model=Any,
        responses={"422": {"model": HTTPValidationError}},
    )
    def update_item_put(
        item_id: int,
        ship: str = ...,
        q1: Optional[str] = None,
        q2: Optional[int] = None,
        body: Item = ...,
    ) -> Union[Any, HTTPValidationError]:
        pass

    url, params, body_dict = app._process_params(
        "/items/{item_id}/ships/{ship}",
        update_item_put,  # type: ignore [arg-type]
        item_id=1,
        ship="ship",
        q1="q1",
        q2=2,
        body=Item(name="name", description="description", price=1.0, tax=1.0),
    )
    assert url == "http://localhost:8080/items/1/ships/ship"
    assert params == {"q1": "q1", "q2": 2}
    assert body_dict == {
        "json": {
            "name": "name",
            "description": "description",
            "price": 1.0,
            "tax": 1.0,
        },
        "headers": {"Content-Type": "application/json"},
    }


def test_process_params_with_query_params_only(app: OpenAPI) -> None:
    @app.get(
        "/items",
        response_model=Any,
        responses={"422": {"model": HTTPValidationError}},
    )
    def update_item_get(
        q1: Optional[str] = None,
        q2: Optional[int] = None,
        body: Item = ...,
    ) -> Union[Any, HTTPValidationError]:
        pass

    url, params, body_dict = app._process_params(
        "/items",
        update_item_get,  # type: ignore [arg-type]
        q1="q1",
        q2=2,
        body=Item(name="name", description="description", price=1.0, tax=1.0),
    )
    assert url == "http://localhost:8080/items"
    assert params == {"q1": "q1", "q2": 2}
    assert body_dict == {
        "json": {
            "name": "name",
            "description": "description",
            "price": 1.0,
            "tax": 1.0,
        },
        "headers": {"Content-Type": "application/json"},
    }


def test_process_params_with_path_params_only(app: OpenAPI) -> None:
    @app.post(
        "/items/{item_id}/ships/{ship}",
        response_model=Any,
        responses={"422": {"model": HTTPValidationError}},
    )
    def update_item_post(
        item_id: int,
        ship: str = ...,
        body: Item = ...,
    ) -> Union[Any, HTTPValidationError]:
        pass

    url, params, body_dict = app._process_params(
        "/items/{item_id}/ships/{ship}",
        update_item_post,  # type: ignore [arg-type]
        item_id=1,
        ship="ship",
        body=Item(name="name", description="description", price=1.0, tax=1.0),
    )
    assert url == "http://localhost:8080/items/1/ships/ship"
    assert params == {}
    assert body_dict == {
        "json": {
            "name": "name",
            "description": "description",
            "price": 1.0,
            "tax": 1.0,
        },
        "headers": {"Content-Type": "application/json"},
    }


def test_process_params_with_no_query_params_or_path_params(app: OpenAPI) -> None:
    @app.delete(
        "/items",
        response_model=Any,
        responses={"422": {"model": HTTPValidationError}},
    )
    def delete_items() -> Union[Any, HTTPValidationError]:
        pass

    url, params, body_dict = app._process_params("/items", delete_items)  # type: ignore [arg-type]
    assert url == "http://localhost:8080/items"
    assert params == {}
    assert body_dict == {"headers": {"Content-Type": "application/json"}}


def test_client_put(monkeypatch: pytest.MonkeyPatch, app: OpenAPI) -> None:
    @app.put(
        "/items/{item_id}/ships/{ship}",
        response_model=Item,
        responses={"422": {"model": HTTPValidationError}},
    )
    def update_item_put(
        item_id: int,
        ship: str = ...,
        q1: Optional[str] = None,
        q2: Optional[int] = None,
        body: Item = ...,
    ) -> Union[Any, HTTPValidationError]:
        pass

    def mock_requests_put(
        url: str, params: dict[str, Any], **body_dict: Any
    ) -> MockResponse:
        json_resp: dict[str, Any] = {
            "name": body_dict["json"]["name"],
            "description": body_dict["json"]["description"],
            "price": body_dict["json"]["price"],
            "tax": body_dict["json"]["tax"],
        }
        return MockResponse(json_resp, 200)

    monkeypatch.setattr(requests, "put", mock_requests_put)

    response_json = update_item_put(  # type: ignore [operator]
        item_id=1,
        ship="ship",
        q1="q1",
        q2="q2",
        body=Item(name="name", description="description", price=1.0, tax=1.0),
    )
    assert response_json == {
        "name": "name",
        "description": "description",
        "price": 1.0,
        "tax": 1.0,
    }


def test_client_post(monkeypatch: pytest.MonkeyPatch, app: OpenAPI) -> None:
    @app.post(
        "/items/{item_id}/ships/{ship}",
        response_model=Item,
        responses={"422": {"model": HTTPValidationError}},
    )
    def update_item_post(
        item_id: int,
        ship: str = ...,
        body: Item = ...,
    ) -> Union[Any, HTTPValidationError]:
        pass

    def mock_requests_post(
        url: str, params: dict[str, Any], **body_dict: Any
    ) -> MockResponse:
        json_resp: dict[str, Any] = {
            "name": body_dict["json"]["name"],
            "description": body_dict["json"]["description"],
            "price": body_dict["json"]["price"],
            "tax": body_dict["json"]["tax"],
        }
        return MockResponse(json_resp, 200)

    monkeypatch.setattr(requests, "post", mock_requests_post)

    response_json = update_item_post(  # type: ignore [operator]
        item_id=1,
        ship="ship",
        q1="q1",
        q2="q2",
        body=Item(name="name", description="description", price=1.0, tax=1.0),
    )
    assert response_json == {
        "name": "name",
        "description": "description",
        "price": 1.0,
        "tax": 1.0,
    }


def test_client_get(monkeypatch: pytest.MonkeyPatch, app: OpenAPI) -> None:
    @app.get(
        "/items",
        response_model=list[Item],
        responses={"422": {"model": HTTPValidationError}},
    )
    def update_items() -> Union[Any, HTTPValidationError]:
        pass

    def mock_requests_get(
        url: str, params: dict[str, Any], **body_dict: Any
    ) -> MockResponse:
        json_resp: list[dict[str, Any]] = [
            {
                "name": "name",
                "description": "description",
                "price": 1.0,
                "tax": 1.0,
            },
            {
                "name": "name2",
                "description": "description2",
                "price": 2.0,
                "tax": 2.0,
            },
        ]
        return MockResponse(json_resp, 200)

    monkeypatch.setattr(requests, "get", mock_requests_get)

    response_json = update_items()  # type: ignore [operator]
    assert response_json == [
        {
            "name": "name",
            "description": "description",
            "price": 1.0,
            "tax": 1.0,
        },
        {
            "name": "name2",
            "description": "description2",
            "price": 2.0,
            "tax": 2.0,
        },
    ]


def test_client_delete(monkeypatch: pytest.MonkeyPatch, app: OpenAPI) -> None:
    @app.delete(
        "/item",
        response_model=None,
        responses={"422": {"model": HTTPValidationError}},
    )
    def delete_item(
        item_id: int,
    ) -> Union[Any, HTTPValidationError]:
        pass

    def mock_requests_delete(
        url: str, params: dict[str, Any], **body_dict: Any
    ) -> MockResponse:
        json_resp: dict[str, Any] = {}

        return MockResponse(json_resp, 200)

    monkeypatch.setattr(requests, "delete", mock_requests_delete)

    response_json = delete_item(item_id=1)  # type: ignore [operator]
    assert response_json == {}
