from typing import Optional

import pytest
from fastapi_code_generator.parser import OpenAPIParser, ParameterObject

from fastagency.openapi.fastapi_code_generator_helpers import patch_get_parameter_type


class TestPatching:
    @pytest.mark.parametrize("description", [None, "Amount in USD to charge"])
    @pytest.mark.parametrize("default_value", [None, 3.14])
    def test_patch_get_parameter_type(
        self, description: Optional[str], default_value: Optional[float]
    ) -> None:
        parser = OpenAPIParser("openapi.json")
        schema = {"type": "number"}
        if default_value is not None:
            schema["default"] = default_value  # type: ignore[assignment]

        parameter = ParameterObject(
            name="amount",
            in_="query",
            description=description,
            required=False,
            schema=schema,
        )
        with patch_get_parameter_type():
            expected_model_dump = {
                "name": "amount",
                "type_hint": "Optional[float]",
                "default": str(default_value) if default_value is not None else None,
                "default_value": str(default_value)
                if default_value is not None
                else None,
                "required": False,
                "description": description,
            }
            parameter_type = parser.get_parameter_type(parameter, True, [])
            assert parameter_type.model_dump() == expected_model_dump

            expected_argument = (
                f"amount: Optional[float] = {default_value}"
                if description is None
                else f'amount: Annotated[Optional[float], """Amount in USD to charge"""] = {default_value}'
            )
            assert parameter_type.argument == expected_argument
