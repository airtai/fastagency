import os
from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from fastagency.app import FastAgency

# Import the function we want to test
from fastagency.cli.discover import get_import_string, import_from_string


@pytest.fixture(scope="module")
def import_fixture() -> Generator[dict[str, Any], None, None]:
    # Create a temporary file for testing
    file_content = """
from fastagency.ui.console import ConsoleUI
from fastagency.runtime.autogen.base import AutoGenWorkflows
from fastagency import FastAgency

wf = AutoGenWorkflows()

app = FastAgency(wf=wf, ui=ConsoleUI())

"""
    with TemporaryDirectory() as tmp_dir:
        try:
            # save old working directory
            old_cwd = Path.cwd()

            # set new working directory
            os.chdir(tmp_dir)

            # Write the content to a temporary Python file
            app_path = Path("test/test_app.py")
            init_path = Path("test/__init__.py")
            app_path.parent.mkdir(parents=True, exist_ok=True)

            with app_path.open("w") as f:
                f.write(file_content)

            with init_path.open("w") as f:
                f.write("")

            # Yield control back to the tests
            import_string, _ = get_import_string(path=app_path, app_name="app")
            yield {
                "import_string": import_string,
                "path": "test/test_app.py",
                "app_name": "app",
            }
        finally:
            # Restore the old working directory
            os.chdir(old_cwd)


class TestGetImportString:
    def test_get_import_string(self, import_fixture: dict[str, Any]) -> None:
        """Test that the import string is correct."""
        path, app_name = import_fixture["path"], import_fixture["app_name"]
        import_string, app = get_import_string(path=Path(path), app_name=app_name)
        assert import_string == "test.test_app:app"
        assert app is not None, "The app should be imported successfully."
        assert isinstance(
            app, FastAgency
        ), "The imported object should be a FastAgency object."


class TestImportFromString:
    def test_import_string(self, import_fixture: dict[str, Any]) -> None:
        """Test that the import string is correct."""
        import_string = import_fixture["import_string"]
        assert import_string == "test.test_app:app"

    def test_import_valid_app(self, import_fixture: dict[str, Any]) -> None:
        """Test importing a valid app from a Python file."""
        import_string = import_fixture["import_string"]

        app = import_from_string(import_string)
        assert app is not None, "The app should be imported successfully."

    def test_import_file_not_found(self) -> None:
        """Test when the specified file doesn't exist."""
        with pytest.raises(
            ImportError, match="The file for module 'nonexistent' does not exist."
        ):
            import_from_string("nonexistent:app")

    def test_import_invalid_format(self) -> None:
        """Test when the import string format is invalid (no colon)."""
        with pytest.raises(
            ImportError,
            match="Import string must be in 'module_name:attribute_name' format.",
        ):
            import_from_string("invalidformat")

    def test_import_module_not_found(self) -> None:
        """Test when the module exists but can't be imported."""
        with pytest.raises(
            ImportError, match="The file for module 'invalid_module' does not exist."
        ):
            import_from_string("invalid_module:app")

    def test_import_attribute_not_found(self, import_fixture: dict[str, Any]) -> None:
        """Test when the module exists but the attribute doesn't."""
        import_string = import_fixture["import_string"]
        test_module, _ = import_string.split(":")
        with pytest.raises(
            ImportError,
            match="Attribute 'nonexistent' not found in module 'test.test_app'.",
        ):
            import_from_string(f"{test_module}:nonexistent")
