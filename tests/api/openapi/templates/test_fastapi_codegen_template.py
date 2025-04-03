import importlib
import sys
import tempfile
from pathlib import Path

import pytest
from datamodel_code_generator import DataModelType
from fastapi_code_generator.__main__ import generate_code

from fastagency.api.openapi import OpenAPI

OPENAPI_FILE_PATHS = list(Path(__file__).parent.glob("*.json"))
TEMPLATE_DIR = Path(__file__).parents[4] / "templates"

assert TEMPLATE_DIR.exists(), TEMPLATE_DIR


@pytest.mark.parametrize(
    "openapi_file_path", OPENAPI_FILE_PATHS, ids=[p.name for p in OPENAPI_FILE_PATHS]
)
def test_fastapi_codegen_template(openapi_file_path: Path) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        td = Path(temp_dir)

        generate_code(
            input_name=openapi_file_path.name,
            input_text=openapi_file_path.read_text(),
            encoding="utf-8",
            output_dir=td,
            template_dir=TEMPLATE_DIR,
            output_model_type=DataModelType.PydanticV2BaseModel,
            custom_visitors=[
                Path(__file__).parents[4]
                / "fastagency"
                / "api"
                / "openapi"
                / "security_schema_visitor.py"
            ],
        )

        main_path = td / "main.py"
        with open(main_path) as f:  # noqa: PTH123
            main_py_code = f.read()
        main_py_code = main_py_code.replace("from .models import", "from models import")
        with open(main_path, "w") as f:  # noqa: PTH123
            f.write(main_py_code)

        original_sys_path = sys.path.copy()
        # add td to sys.path
        try:
            sys.path.append(str(td))
            importlib.invalidate_caches()

            if "main" in sys.modules:
                del sys.modules["main"]
            if "models" in sys.modules:
                del sys.modules["models"]

            main = importlib.import_module("main", package=td.name)  # nosemgrep
            importlib.reload(main)
        finally:
            sys.path = original_sys_path

        app = main.app
        assert app._title == openapi_file_path.stem


@pytest.mark.parametrize("openapi_file_path", OPENAPI_FILE_PATHS)
def test_fastapi_codegen_template_openapi(openapi_file_path: Path) -> None:
    app = OpenAPI.create(openapi_json=openapi_file_path.read_text())
    assert isinstance(app, OpenAPI)
