from ...helpers import check_imports

check_imports(["fastapi_code_generator", "fastapi", "requests"], "openapi")

from .patch_datamodel_code_generator import patch_apply_discriminator_type  # noqa: E402
from .patch_fastapi_code_generator import (  # noqa: E402
    patch_function_name_parsing,
    patch_generate_code,
    patch_parse_schema,
)

patch_parse_schema()
patch_function_name_parsing()
patch_generate_code()
patch_apply_discriminator_type()

from .client import OpenAPI  # noqa: E402

__all__ = ["OpenAPI"]
