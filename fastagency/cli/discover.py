import importlib
import sys
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Tuple, Union

from rich import print
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.tree import Tree

from .. import FastAgency
from ..exceptions import FastAgencyCLIError

logger = getLogger(__name__)


def get_default_path() -> Path:
    potential_paths = (
        "main.py",
        "app.py",
        "api.py",
        "app/main.py",
        "app/app.py",
        "app/api.py",
    )

    for full_path in potential_paths:
        path = Path(full_path)
        if path.is_file():
            return path

    raise FastAgencyCLIError(
        "Could not find a default file to run, please provide an explicit path"
    )


@dataclass
class ModuleData:
    module_import_str: str
    extra_sys_path: Path


def get_module_data_from_path(path: Path) -> ModuleData:
    logger.info(
        "Searching for package file structure from directories with [blue]__init__.py[/blue] files"
    )
    use_path = path.resolve()
    module_path = use_path
    if use_path.is_file() and use_path.stem == "__init__":
        module_path = use_path.parent
    module_paths = [module_path]
    extra_sys_path = module_path.parent
    for parent in module_path.parents:
        init_path = parent / "__init__.py"
        if init_path.is_file():
            module_paths.insert(0, parent)
            extra_sys_path = parent.parent
        else:
            break
    logger.info(f"Importing from {extra_sys_path.resolve()}")
    root = module_paths[0]
    name = f"🐍 {root.name}" if root.is_file() else f"📁 {root.name}"
    root_tree = Tree(name)
    if root.is_dir():
        root_tree.add("[dim]🐍 __init__.py[/dim]")
    tree = root_tree
    for sub_path in module_paths[1:]:
        sub_name = (
            f"🐍 {sub_path.name}" if sub_path.is_file() else f"📁 {sub_path.name}"
        )
        tree = tree.add(sub_name)
        if sub_path.is_dir():
            tree.add("[dim]🐍 __init__.py[/dim]")
    title = "[b green]Python module file[/b green]"
    if len(module_paths) > 1 or module_path.is_dir():
        title = "[b green]Python package file structure[/b green]"
    panel = Padding(
        Panel(
            root_tree,
            title=title,
            expand=False,
            padding=(1, 2),
        ),
        1,
    )
    print(panel)
    module_str = ".".join(p.stem for p in module_paths)
    logger.info(f"Importing module [green]{module_str}[/green]")
    return ModuleData(
        module_import_str=module_str,
        extra_sys_path=extra_sys_path.resolve(),
    )


def get_app_name(  # noqa: C901
    *, mod_data: ModuleData, app_name: Union[str, None] = None
) -> "Tuple[str, FastAgency]":
    try:
        mod = importlib.import_module(mod_data.module_import_str)  # nosemgrep
    except (ImportError, ValueError) as e:
        logger.error(f"Import error: {e}")
        logger.warning(
            "Ensure all the package directories have an [blue]__init__.py[/blue] file"
        )
        raise
    if not FastAgency:  # type: ignore[truthy-function]
        raise FastAgencyCLIError(
            "Could not import FastAgency, try running 'pip install fastagency'"
        ) from None
    object_names = dir(mod)
    object_names_set = set(object_names)
    if app_name:
        if app_name not in object_names_set:
            raise FastAgencyCLIError(
                f"Could not find app name {app_name} in {mod_data.module_import_str}"
            )
        app = getattr(mod, app_name)
        if not isinstance(app, FastAgency):
            raise FastAgencyCLIError(
                f"The app name {app_name} in {mod_data.module_import_str} doesn't seem to be a FastAgency app"
            )
        return app_name, app
    for preferred_name in ["app", "api"]:
        if preferred_name in object_names_set:
            obj = getattr(mod, preferred_name)
            if isinstance(obj, FastAgency):
                return preferred_name, obj
    for name in object_names:
        obj = getattr(mod, name)
        if isinstance(obj, FastAgency):
            return name, obj
    raise FastAgencyCLIError("Could not find FastAgency app in module, try using --app")


def get_import_string(
    *, path: Union[Path, None] = None, app_name: Union[str, None] = None
) -> tuple[str, FastAgency]:
    if not path:
        path = get_default_path()
    logger.info(f"Using path [blue]{path}[/blue]")
    logger.info(f"Resolved absolute path {path.resolve()}")
    if not path.exists():
        raise FastAgencyCLIError(f"Path does not exist {path}")
    mod_data = get_module_data_from_path(path)
    sys.path.insert(0, str(mod_data.extra_sys_path))
    use_app_name, app = get_app_name(mod_data=mod_data, app_name=app_name)
    import_example = Syntax(
        f"from {mod_data.module_import_str} import {use_app_name}", "python"
    )
    import_panel = Padding(
        Panel(
            import_example,
            title="[b green]Importable FastAgency app[/b green]",
            expand=False,
            padding=(1, 2),
        ),
        1,
    )
    logger.info("Found importable FastAgency app")
    print(import_panel)
    import_string = f"{mod_data.module_import_str}:{use_app_name}"
    logger.info(f"Using import string [b green]{import_string}[/b green]")
    return import_string, app


def import_from_string(import_string: str) -> FastAgency:
    """Import a module and attribute from an import string.

    Import a module and an attribute from a string like 'file_name:app_name'.
    Checks if the file exists before attempting to import the module.

    Args:
        import_string (str): The import string in 'module_name:attribute_name' format.

    Returns:
        Any: The attribute from the module.

    Raises:
        ImportError: If the import string is not in the correct format or the module or attribute is not found.
        ValueError: If the import string is not in 'module_name:attribute_name' format.
        ModuleNotFoundError: If the module is not found.
        AttributeError: If the attribute is not found in the module.

    """
    try:
        # Split the string into module and attribute parts
        module_name, attribute_name = import_string.split(":")

        # Ensure the module name points to a valid Python file before importing
        module_path = f"{module_name.replace('.', '/')}.py"
        if not Path(module_path).is_file():
            raise ImportError(f"The file for module '{module_name}' does not exist.")

        # Add the current directory to the Python path to allow imports from local files
        sys.path.append(str(Path.cwd()))

        # Import the module using importlib
        module = importlib.import_module(module_name)  # nosemgrep

        # Get the attribute (like 'app') from the module
        attribute = getattr(module, attribute_name)
        if not isinstance(attribute, FastAgency):
            raise ImportError(
                f"The attribute '{attribute_name}' in module '{module_name}' is not a FastAgency app."
            )

        return attribute
    except ValueError:
        raise ImportError(
            "Import string must be in 'module_name:attribute_name' format."
        ) from None
    except ModuleNotFoundError:
        raise ImportError(f"Module '{module_name}' not found.") from None
    except AttributeError:
        raise ImportError(
            f"Attribute '{attribute_name}' not found in module '{module_name}'."
        ) from None
