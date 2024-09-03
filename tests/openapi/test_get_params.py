from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field

from fastagency.openapi.client import Client


class Item(BaseModel):
    name: str = Field(..., description="Name of the item", title="Name")
    description: str = Field(
        ..., description="Description of the item", title="Description"
    )
    price: float = Field(..., description="Price of the item", title="Price")
    tax: float = Field(..., description="Tax of the item", title="Tax")


class ValidationError(BaseModel):
    loc: List[Union[str, int]] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title="Detail")


app = Client(
    title="FastAPI",
    version="0.1.0",
    servers=[{"url": "http://localhost:8080", "description": "Local environment"}],
)


def test_get_params_with_query_params_and_path_params() -> None:
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

    query_params, path_params, body, security = Client._get_params(
        "/items/{item_id}/ships/{ship}",
        update_item_put,  # type: ignore [arg-type]
    )

    assert query_params == {"q1", "q2"}
    assert path_params == {"item_id", "ship"}
    assert body == "body"


def test_get_params_with_query_params_only() -> None:
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

    query_params, path_params, body, security = Client._get_params(
        "/items",
        update_item_get,  # type: ignore [arg-type]
    )
    assert query_params == {"q1", "q2"}
    assert path_params == set()
    assert body == "body"


def test_get_params_with_path_params_only() -> None:
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

    query_params, path_params, body, security = Client._get_params(
        "/items/{item_id}/ships/{ship}",
        update_item_post,  # type: ignore [arg-type]
    )

    assert query_params == set()
    assert path_params == {"item_id", "ship"}
    assert body == "body"


def test_get_params_with_no_query_params_or_path_params() -> None:
    @app.delete(
        "/items",
        response_model=Any,
        responses={"422": {"model": HTTPValidationError}},
    )
    def delete_items() -> Union[Any, HTTPValidationError]:
        pass

    query_params, path_params, body, security = Client._get_params(
        "/items",
        delete_items,  # type: ignore [arg-type]
    )

    assert query_params == set()
    assert path_params == set()
    assert body is None
