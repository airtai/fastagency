import time
from collections.abc import Iterator
from platform import system
from typing import Annotated

import pytest
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyCookie, APIKeyHeader

from ....conftest import Server, find_free_port


def create_secure_fastapi_app(host: str, port: int) -> FastAPI:
    app = FastAPI(servers=[{"url": f"http://{host}:{port}"}])

    api_key = "super secret key"  # pragma: allowlist secret
    api_key_name = "access_token"  # pragma: allowlist secret

    header_scheme = APIKeyHeader(name=api_key_name, auto_error=False)
    cookie_scheme = APIKeyCookie(name=api_key_name, auto_error=False)

    async def get_api_key(
        api_key_header: str = Depends(header_scheme),
        api_key_cookie: str = Depends(cookie_scheme),
    ) -> str:
        if api_key_header == api_key:
            return api_key_header
        elif api_key_cookie == api_key:
            return api_key_cookie
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

    @app.get("/items/")
    async def read_items(
        city: Annotated[str, Query(description="city for which forecast is requested")],
        api_key: str = Depends(get_api_key),
    ) -> JSONResponse:
        content = {"api_key": api_key}
        status_code = 200
        return JSONResponse(status_code=status_code, content=content)

    return app


@pytest.fixture(scope="session")
def secure_fastapi_url() -> Iterator[str]:
    host = "127.0.0.1"
    port = find_free_port()
    app = create_secure_fastapi_app(host, port)

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = Server(config=config)
    with server.run_in_thread():
        time.sleep(1 if system() != "Windows" else 5)  # let the server start

        yield f"http://{host}:{port}"
