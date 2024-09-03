from typing import Annotated
from fastapi import Depends, FastAPI, Query
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse

app = FastAPI(servers=[{"url": "http://localhost:8888"}])

header_scheme = APIKeyHeader(name="x-key")

UNIVERSAL_API_KEY = "super secret key"

@app.get("/items/")
async def read_items(city: Annotated[str, Query(description="city for which forecast is requested")], key: str = Depends(header_scheme)):
    is_authenticated = key == UNIVERSAL_API_KEY
    content = {"is_authenticated": is_authenticated}
    status_code = 200 if is_authenticated else 403
    return JSONResponse(status_code=status_code, content=content)
