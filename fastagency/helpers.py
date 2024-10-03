import importlib
import json
from collections.abc import Iterator
from json import JSONDecoder
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
        match = text.find("{", pos)
        if match == -1:
            yield text[pos:]  # return the remaining text
            break
        # move past space characters if needed
        while text[pos] == " ":
            pos += 1
        yield text[pos:match]  # modification for the non-JSON parts
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
            # move past space characters if needed
            while text[pos] == " ":
                pos += 1
        except ValueError:
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
