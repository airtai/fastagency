import importlib
import pkgutil
import sys  # Import the pkgutil module to work with the import system

import pytest

from fastagency.exceptions import (
    FastAgencyCLIPythonVersionError,  # Import the importlib module to dynamically import modules
)


def list_submodules(module_name: str) -> list[str]:
    """List all submodules of a given module.

    Args:
        module_name (str): The name of the module to list submodules for.

    Returns:
        list: A list of submodule names.
    """
    # Import the module dynamically using its name
    try:
        module = importlib.import_module(module_name)
    except Exception:
        return []

    # Get the path of the module. This is necessary to find its submodules.
    module_path = module.__path__

    # Initialize an empty list to store the names of submodules
    submodules = []

    # Iterate over the submodules in the module's path
    for _, name, ispkg in pkgutil.iter_modules(module_path, prefix=f"{module_name}."):
        # Add the name of each submodule to the list
        submodules.append(name)

        if ispkg:
            submodules.extend(list_submodules(name))

    # Return the list of submodule names
    return submodules


def test_list_submodules() -> None:
    # Specify the name of the module you want to inspect
    module_name = "fastagency"

    # Get the list of submodules for the specified module
    submodules = list_submodules(module_name)

    assert "fastagency.ui" in submodules
    assert "fastagency.ui.mesop" in submodules
    assert "fastagency.ui.console.base" in submodules


@pytest.mark.parametrize("module", list_submodules("fastagency"))
def test_submodules(module: str) -> None:
    if module.startswith("fastagency.ui.mesop") and sys.version_info < (3, 10):
        with pytest.raises(
            FastAgencyCLIPythonVersionError,
            match="Mesop requires Python 3.10 or higher",
        ):
            importlib.import_module(module)
        return

    importlib.import_module(module)
