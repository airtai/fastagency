import importlib
import sys
import tempfile
from pathlib import Path
from typing import Any, Union

from _pytest.monkeypatch import MonkeyPatch
from fastapi_code_generator.__main__ import generate_code

OPENAPI_FILE_PATH = (Path(__file__).parent / "openapi.json").resolve()
TEMPLATE_DIR = Path(__file__).parent.parent.parent.parent / "templates"

assert OPENAPI_FILE_PATH.exists(), OPENAPI_FILE_PATH
assert TEMPLATE_DIR.exists(), TEMPLATE_DIR


class MockResponse:
    def __init__(
        self, json_data: Union[list[dict[str, Any]], dict[str, Any]], status_code: int
    ) -> None:
        """Mock response object for requests."""
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> Union[list[dict[str, Any]], dict[str, Any]]:
        """Return the json data."""
        return self.json_data


def test_fastapi_codegen_template(monkeypatch: MonkeyPatch) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        td = Path(temp_dir)

        generate_code(
            input_name=OPENAPI_FILE_PATH.name,
            input_text=OPENAPI_FILE_PATH.read_text(),
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
