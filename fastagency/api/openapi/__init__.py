from ...helpers import check_imports

check_imports(["fastapi_code_generator", "fastapi", "requests"], "openapi")

from .client import OpenAPI  # noqa: E402

__all__ = ["OpenAPI"]
