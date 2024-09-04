from pathlib import Path
from typing import Dict

from fastapi_code_generator.parser import OpenAPIParser
from fastapi_code_generator.visitor import Visitor

from fastagency.openapi.security import BaseSecurity


def custom_visitor(parser: OpenAPIParser, model_path: Path) -> Dict[str, object]:
    security_schemes = parser.raw_obj["components"]["securitySchemes"]

    # for k, v in security_schemes.items():
    #     security_schemes[k]["in_value"] = security_schemes[k].pop("in")

    security_classes = []
    security_parameters = {}
    for k, v in security_schemes.items():
        security_class = BaseSecurity.get_security_class(
            type=v["type"], in_value=v["in"]
        )
        security_classes.append(security_class)
        name = v["name"]
        security_parameters[k] = f'{security_class}(name="{name}")'

    return {
        "security_schemes": security_schemes,
        "security_classes": security_classes,
        "security_parameters": security_parameters,
    }


visit: Visitor = custom_visitor
