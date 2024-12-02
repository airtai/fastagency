import os
import random
import shutil
import sys
from collections.abc import Generator, Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from fastagency.app import FastAgency

# Import the function we want to test
from fastagency.cli.discover import (
    ModuleData,
    get_app_name,
    get_default_path,
    get_import_string,
    get_module_data_from_path,
    import_from_string,
)
from fastagency.exceptions import FastAgencyCLIError


@contextmanager
def _import_fixture(
    mock_app: bool = False, missing_init: bool = False, syntax_error: bool = False
) -> Generator[dict[str, Any], None, None]:
    # Create a temporary file for testing
    main_content = f"""
from unittest.mock import MagicMock
from fastagency.ui.console import ConsoleUI
from fastagency.runtimes.ag2 import AutoGenWorkflows
{'frim' if syntax_error else 'from'} fastagency import FastAgency


wf = AutoGenWorkflows()

app = {'FastAgency(provider=wf, ui=ConsoleUI())' if not mock_app else 'MagicMock()'}

"""

    init_content = """
from .test_app import app
"""

    with TemporaryDirectory() as tmp_dir:
        try:
            # save old working directory
            old_cwd = Path.cwd()

            # set new working directory
            os.chdir(tmp_dir)

            # Write the content to a temporary Python file
            suffix = random.randint(1_000_000_000, 1_000_000_000_000 - 1)
            mod_name = f"test-{suffix:d}"
            app_path = Path(mod_name) / "test_app.py"
            init_path = Path(mod_name) / "__init__.py"
            app_path.parent.mkdir(parents=True, exist_ok=True)

            with app_path.open("w") as f:
                f.write(main_content)

            if not missing_init:
                with init_path.open("w") as f:
                    f.write(init_content)

            # Yield control back to the tests
            # import_string, _ = get_import_string(path=app_path, app_name="app")
            yield {
                "import_string": f"{mod_name}.test_app:app",
                "path": f"{mod_name}/test_app.py",
                "init_path": f"{mod_name}/__init__.py",
                "app_name": "app",
                "mod_name": mod_name,
            }
        finally:
            # Restore the old working directory
            os.chdir(old_cwd)


@pytest.fixture
def import_fixture() -> Generator[dict[str, Any], None, None]:
    with _import_fixture() as fixture:
        yield fixture


@pytest.fixture
def import_fixture_mocked_app() -> Generator[dict[str, Any], None, None]:
    with _import_fixture(mock_app=True) as fixture:
        yield fixture


@pytest.fixture
def import_fixture_missing_init() -> Generator[dict[str, Any], None, None]:
    with _import_fixture(missing_init=True) as fixture:
        yield fixture


@pytest.fixture
def import_fixture_syntax_error() -> Generator[dict[str, Any], None, None]:
    with _import_fixture(syntax_error=True) as fixture:
        yield fixture


class TestGetAppName:
    @contextmanager
    def _get_mod_data(self, path: str) -> Iterator[ModuleData]:
        mod_data = get_module_data_from_path(Path(path))
        system_path_updated = False
        try:
            sys.path.insert(0, str(mod_data.extra_sys_path.resolve()))
            system_path_updated = True
            yield mod_data
        finally:
            if system_path_updated:
                sys.path.remove(str(mod_data.extra_sys_path.resolve()))

    @pytest.mark.parametrize("use_app_name", [True, False])
    def test_get_app_name_success(
        self, import_fixture: dict[str, Any], use_app_name: bool
    ) -> None:
        """Test that the app name is correct."""
        path, app_name = import_fixture["path"], import_fixture["app_name"]
        with self._get_mod_data(path) as mod_data:
            if use_app_name:
                app_name, app = get_app_name(mod_data=mod_data, app_name=app_name)
            else:
                app_name, app = get_app_name(mod_data=mod_data)
            assert app_name == "app"
            assert app is not None, "The app should be imported successfully."
            assert isinstance(
                app, FastAgency
            ), "The imported object should be a FastAgency object."

    def test_get_app_name_syntax_error(
        self, import_fixture_syntax_error: dict[str, Any]
    ) -> None:
        path, app_name = (
            import_fixture_syntax_error["path"],
            import_fixture_syntax_error["app_name"],
        )
        with self._get_mod_data(path) as mod_data:  # noqa: SIM117
            with pytest.raises(SyntaxError, match="invalid syntax"):
                get_app_name(mod_data=mod_data, app_name=app_name)

    def test_get_app_name_import_error(
        self, import_fixture_syntax_error: dict[str, Any]
    ) -> None:
        with self._get_mod_data("something_random") as mod_data:  # noqa: SIM117
            with pytest.raises(ImportError, match="No module named 'something_random'"):
                get_app_name(mod_data=mod_data)

    def test_get_app_name_mocked_app(
        self, import_fixture_mocked_app: dict[str, Any]
    ) -> None:
        path = import_fixture_mocked_app["path"]
        app_name = import_fixture_mocked_app["app_name"]
        mod_name = import_fixture_mocked_app["mod_name"]
        with self._get_mod_data(path) as mod_data:  # noqa: SIM117
            with pytest.raises(
                FastAgencyCLIError,
                match=f"The app name app in {mod_name}.test_app doesn't seem to be a FastAgency app",
            ):
                app_name, app = get_app_name(mod_data=mod_data, app_name=app_name)


class TestGetImportString:
    def test_get_import_string_success(self, import_fixture: dict[str, Any]) -> None:
        """Test that the import string is correct."""
        path, app_name = import_fixture["path"], import_fixture["app_name"]
        import_string, app = get_import_string(path=Path(path), app_name=app_name)
        mod_name = import_fixture["mod_name"]
        assert import_string == f"{mod_name}.test_app:app"
        assert app is not None, "The app should be imported successfully."
        assert isinstance(
            app, FastAgency
        ), "The imported object should be a FastAgency object."

    @pytest.mark.skip("This test is not working as expected.")
    def test_get_import_string_default_path_success(
        self, import_fixture: dict[str, Any]
    ) -> None:
        """Test that the import string is correct."""
        path, _ = import_fixture["path"], import_fixture["app_name"]
        shutil.copy2(Path(path), Path("main.py"))
        import_string, app = get_import_string()
        assert import_string == "main:app"
        assert app is not None, "The app should be imported successfully."
        assert isinstance(
            app, FastAgency
        ), "The imported object should be a FastAgency object."

    def test_get_import_string_missing_path(self) -> None:
        """Test that the import string is correct."""
        with pytest.raises(FastAgencyCLIError, match="Path does not exist"):
            get_import_string(path=Path("some_random_name.py"))

    def test_get_import_string_missing_app_name(
        self, import_fixture: dict[str, Any]
    ) -> None:
        path, app_name = import_fixture["path"], import_fixture["app_name"]
        mod_name = import_fixture["mod_name"]
        assert app_name == "app"

        import_string, app = get_import_string(path=Path(path))

        assert import_string == f"{mod_name}.test_app:app"
        assert app is not None, "The app should be imported successfully."
        assert isinstance(
            app, FastAgency
        ), "The imported object should be a FastAgency object."

    def test_get_import_string_missing_init(
        self, import_fixture_missing_init: dict[str, Any]
    ) -> None:
        path, app_name = (
            import_fixture_missing_init["path"],
            import_fixture_missing_init["app_name"],
        )
        path = path.split("/")[0]
        with pytest.raises(
            FastAgencyCLIError, match="Could not find app name app in test"
        ):
            get_import_string(path=Path(path), app_name=app_name)

    def test_get_import_string_syntax_error(
        self, import_fixture_syntax_error: dict[str, Any]
    ) -> None:
        path, app_name = (
            import_fixture_syntax_error["path"],
            import_fixture_syntax_error["app_name"],
        )
        path = path.split("/")[0]
        with pytest.raises(SyntaxError, match="invalid syntax"):
            get_import_string(path=Path(path), app_name=app_name)

    def test_get_import_init(self, import_fixture: dict[str, Any]) -> None:
        """Test that the import string is correct."""
        init_path, _ = import_fixture["init_path"], import_fixture["app_name"]
        import_string, app = get_import_string(path=Path(init_path))
        mod_name = import_fixture["mod_name"]
        assert import_string == f"{mod_name}:app"
        assert app is not None, "The app should be imported successfully."
        assert isinstance(
            app, FastAgency
        ), "The imported object should be a FastAgency object."

    def test_get_import_dir(self, import_fixture: dict[str, Any]) -> None:
        """Test that the import string is correct."""
        init_path, _ = import_fixture["init_path"], import_fixture["app_name"]
        dir_path = Path(init_path).parent
        import_string, app = get_import_string(path=dir_path)

        mod_name = import_fixture["mod_name"]
        assert import_string == f"{mod_name}:app"
        assert app is not None, "The app should be imported successfully."
        assert isinstance(
            app, FastAgency
        ), "The imported object should be a FastAgency object."


class TestImportFromString:
    def test_import_string(self, import_fixture: dict[str, Any]) -> None:
        """Test that the import string is correct."""
        import_string = import_fixture["import_string"]
        mod_name = import_fixture["mod_name"]
        assert import_string == f"{mod_name}.test_app:app"

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
        mod_name = import_fixture["mod_name"]
        with pytest.raises(
            ImportError,
            match=f"Attribute 'nonexistent' not found in module '{mod_name}.test_app'.",
        ):
            import_from_string(f"{test_module}:nonexistent")

    def test_not_fastagency_app(
        self, import_fixture_mocked_app: dict[str, Any]
    ) -> None:
        """Test when the attribute is not a FastAgency app."""
        import_string = import_fixture_mocked_app["import_string"]
        test_module, _ = import_string.split(":")
        with pytest.raises(
            ImportError,
            match="Import string must be in 'module_name:attribute_name' format.",
        ):
            import_from_string(test_module)


class TestGetDefaultPath:
    @contextmanager
    def _create_empty_path(self, path: str) -> Iterator[Path]:
        with TemporaryDirectory() as tmp_dir:
            # save old working directory
            old_cwd = Path.cwd()

            # set new working directory
            try:
                os.chdir(tmp_dir)

                # Write the content to a temporary Python file
                p = Path(path)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.touch()

                yield p
            finally:
                # Restore the old working directory
                os.chdir(old_cwd)

    @pytest.mark.parametrize(
        "potential_path",
        [
            "main.py",
            "app.py",
            "api.py",
            "app/main.py",
            "app/app.py",
            "app/api.py",
        ],
    )
    def test_get_default_path_success(self, potential_path: str) -> None:
        """Test that the correct default path is returned."""
        with self._create_empty_path(potential_path) as p:
            assert get_default_path() == p
            assert str(get_default_path()) == str(p), f"{get_default_path=}, {p=}"

    def test_get_default_path_missing(self) -> None:
        """Test that the correct default path is returned."""
        with self._create_empty_path("random_stuff.py"):  # noqa: SIM117
            with pytest.raises(FastAgencyCLIError):
                get_default_path()
