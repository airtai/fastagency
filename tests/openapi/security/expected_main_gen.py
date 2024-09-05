# generated by fastapi-codegen:
#   filename:  openapi.json
#   timestamp: 2024-09-04T06:42:36+00:00

from __future__ import annotations

from typing import *
from typing import Any, Union

from fastagency.openapi.client import Client
from fastagency.openapi.security import APIKeyHeader

from models_gen import HTTPValidationError

app = Client(
    title='FastAPI',
    version='0.1.0',
    servers=[{'url': 'http://localhost:9999'}],
)


@app.get(
    '/items/',
    response_model=Any,
    responses={'422': {'model': HTTPValidationError}},
    security=APIKeyHeader(name="x-key"),
)
def read_items_items__get(
    city: Annotated[str, """city for which forecast is requested"""]
) -> Union[Any, HTTPValidationError]:
    """
    Read Items
    """
    pass