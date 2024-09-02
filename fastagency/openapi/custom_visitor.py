from pathlib import Path
from typing import Dict

from fastapi_code_generator.parser import OpenAPIParser
from fastapi_code_generator.visitor import Visitor


def custom_visitor(parser: OpenAPIParser, model_path: Path) -> Dict[str, object]:
    security_schemes = parser.raw_obj["components"]["securitySchemes"]
    # for k, v in security_schemes.items():
    #     security_schemes[k]["in_value"] = security_schemes[k].pop("in")

    return {"security_schemes": security_schemes}


visit: Visitor = custom_visitor
