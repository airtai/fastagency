import re
from functools import cached_property, wraps
from typing import Any

import stringcase
from fastapi_code_generator.parser import OpenAPIParser, Operation

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


def patch_function_name_parsing() -> None:
    def function_name(self: Any) -> str:
        if self.operationId:
            name: str = self.operationId.replace("/", "_")
        else:
            path = re.sub(r"/{|/", "_", self.snake_case_path).replace("}", "")
            name = f"{self.type}{path}"
        return stringcase.snakecase(name)  # type: ignore[no-any-return]

    Operation.function_name = cached_property(function_name)
    Operation.function_name.__set_name__(Operation, "function_name")

    logger.info("Patched Operation.function_name")
