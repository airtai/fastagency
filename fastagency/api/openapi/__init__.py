from ...helpers import check_imports

check_imports(["fastapi_code_generator", "fastapi", "requests"], "openapi")

from .client import OpenAPI  # noqa: E402
from .patch_fastapi_code_generator import patch_parse_schema  # noqa: E402

patch_parse_schema()

__all__ = ["OpenAPI"]
