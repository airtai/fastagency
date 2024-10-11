import importlib
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi_code_generator.__main__ import generate_code

OPENAPI_FILE_PATHS = Path(__file__).parent.glob("*.json")
TEMPLATE_DIR = Path(__file__).parents[4] / "templates"

assert TEMPLATE_DIR.exists(), TEMPLATE_DIR


@pytest.mark.parametrize("openapi_file_path", OPENAPI_FILE_PATHS)
def test_fastapi_codegen_template(openapi_file_path: Path) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        td = Path(temp_dir)

        generate_code(
            input_name=openapi_file_path.name,
            input_text=openapi_file_path.read_text(),
            encoding="utf-8",
            output_dir=td,
            template_dir=TEMPLATE_DIR,
        )

        main_path = td / "main.py"
        with open(main_path) as f:  # noqa: PTH123
            main_py_code = f.read()
        main_py_code = main_py_code.replace("from .models import", "from models import")
        with open(main_path, "w") as f:  # noqa: PTH123
            f.write(main_py_code)

        # add td to sys.path
        try:
            sys.path.append(str(td))
            main = importlib.import_module("main", package=td.name)  # nosemgrep
        finally:
            sys.path.remove(str(td))

        app = main.app
        assert app.title == "FastAPI"
