import importlib

__all__ = ["check_imports"]


def check_imports(package_names: list[str], target_name: str) -> None:
    not_importable = [
        f"'{package_name}'"
        for package_name in package_names
        if importlib.util.find_spec(package_name) is None
    ]
    if len(not_importable) > 0:
        raise ImportError(
            f"Package(s) {', '.join(not_importable)} not found. Please install it with:\n\npip install \"fastagency[{target_name}]\"\n"
        )
