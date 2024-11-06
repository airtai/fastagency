import importlib
import sys  # Import the pkgutil module to work with the import system

import pytest

from fastagency.exceptions import (
    FastAgencyCLIPythonVersionError,  # Import the importlib module to dynamically import modules
)

from .helpers import list_submodules


def test_list_submodules() -> None:
    # Specify the name of the module you want to inspect
    module_name = "fastagency"

    # Get the list of submodules for the specified module
    submodules = list_submodules(module_name)

    assert len(submodules) > 0
    assert "fastagency" in submodules
    assert "fastagency.ui" in submodules
    assert "fastagency.ui.mesop" in submodules
    assert "fastagency.ui.console.console" in submodules


@pytest.mark.parametrize("module", list_submodules("fastagency"))
def test_submodules(module: str) -> None:
    if module.startswith("fastagency.ui.mesop") and sys.version_info < (3, 10):
        with pytest.raises(
            FastAgencyCLIPythonVersionError,
            match="Mesop requires Python 3.10 or higher",
        ):
            importlib.import_module(module)  # nosemgrep
        return

    importlib.import_module(module)  # nosemgrep
