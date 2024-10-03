from pathlib import Path

from fastapi_code_generator.parser import OpenAPIParser
from fastapi_code_generator.visitor import Visitor

from fastagency.api.openapi.security import BaseSecurity


def custom_visitor(parser: OpenAPIParser, model_path: Path) -> dict[str, object]:
    if "securitySchemes" not in parser.raw_obj["components"]:
        return {}
    security_schemes = parser.raw_obj["components"]["securitySchemes"]

    # for k, v in security_schemes.items():
    #     security_schemes[k]["in_value"] = security_schemes[k].pop("in")

    security_classes = []
    security_parameters = {}
    for k, v in security_schemes.items():
        if "in" not in v and v["type"] == "http":
            in_value = v.get("scheme", None)
        if "in" not in v and v["type"] == "oauth2":
            in_value = v.get("flows", None)
        else:
            in_value = v["in"]
        security_class = BaseSecurity.get_security_class(
            type=v["type"], in_value=in_value
        )
        if security_class is None:
            continue
        security_classes.append(security_class)
        name = v.get("name", None)
        security_parameters[k] = f'{security_class}(name="{name}")'

    return {
        "security_schemes": security_schemes,
        "security_classes": security_classes,
        "security_parameters": security_parameters,
    }


visit: Visitor = custom_visitor
