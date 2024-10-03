import importlib
import json
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from json import JSONDecoder
from pathlib import Path
from typing import Optional

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


# based on https://stackoverflow.com/questions/61380028/how-to-detect-and-indent-json-substrings-inside-longer-non-json-text/61384796#61384796
def extract_json_objects(
    text: str, decoder: Optional[JSONDecoder] = None
) -> Iterator[str]:
    decoder = decoder or JSONDecoder()
    pos = 0
    while True:
        # print(f"matching: {text[pos:]}")
        match = text.find("{", pos)
        if match == -1:
            yield text[pos:]  # return the remaining text
            break
        yield text[pos:match].rstrip(" ")  # modification for the non-JSON parts
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
            # move past space characters if needed
            while pos < len(text) and text[pos] == " ":
                pos += 1
        except ValueError:
            yield text[match]
            pos = match + 1


def jsonify_string(line: str) -> str:
    line_parts: list[str] = []
    for result in extract_json_objects(line):
        if isinstance(result, dict):  # got a JSON obj
            line_parts.append(f"\n```\n{json.dumps(result, indent=4)}\n```\n")
        else:  # got text/non-JSON-obj
            line_parts.append(result)
    # (don't make that a list comprehension, quite un-readable)

    return "".join(line_parts)


@contextmanager
def optional_temp_path(path: Optional[str] = None) -> Iterator[Path]:
    if path is None:
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    else:
        yield Path(path)
