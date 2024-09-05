import time
from collections.abc import Iterator
from platform import system
from typing import Annotated

import pytest
import uvicorn
from fastapi import Depends, FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from ...conftest import Server, find_free_port


def create_secure_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(servers=[{"url": f"http://{host}:{port}"}])

    header_scheme = APIKeyHeader(name="x-key")

    universal_api_key = "super secret key"  # pragma: allowlist secret

    @app.get("/items/")
    async def read_items(
        city: Annotated[str, Query(description="city for which forecast is requested")],
        key: str = Depends(header_scheme),
    ) -> JSONResponse:
        is_authenticated = key == universal_api_key
        content = {"is_authenticated": is_authenticated}
        status_code = 200 if is_authenticated else 403
        return JSONResponse(status_code=status_code, content=content)

    return app


@pytest.fixture(scope="session")
def secure_fastapi_url() -> Iterator[str]:
    host = "localhost"
    port = find_free_port()
    app = create_secure_fastapi_app(host, port)

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = Server(config=config)
    with server.run_in_thread():
        time.sleep(1 if system() != "Windows" else 5)  # let the server start

        yield f"http://{host}:{port}"
