from functools import wraps
from typing import Any

from fastapi_code_generator.parser import OpenAPIParser

from ...logging import get_logger

logger = get_logger(__name__)


def patch_parse_schema() -> None:
    org_parse_schema = OpenAPIParser.parse_schema

    @wraps(org_parse_schema)
    def my_parse_schema(*args: Any, **kwargs: Any) -> Any:
        data_type = org_parse_schema(*args, **kwargs)
        if data_type.reference and data_type.reference.duplicate_name:
            data_type.reference.name = data_type.reference.duplicate_name
        return data_type

    OpenAPIParser.parse_schema = my_parse_schema
    logger.info("Patched OpenAPIParser.parse_schema")
