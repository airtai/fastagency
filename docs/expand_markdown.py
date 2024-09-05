"""Expand markdown files with embedded lines from other files."""

import logging
import re
from pathlib import Path
from typing import Annotated, Optional

import typer

logging.basicConfig(level=logging.INFO)


app = typer.Typer()


def _read_lines_from_file(file_path: Path, lines_spec: Optional[str]):
    with file_path.open() as file:
        all_lines = file.readlines()

    # Check if lines_spec is empty (indicating all lines should be read)
    if not lines_spec:
        return "".join(all_lines)

    selected_lines = []
    line_specs = lines_spec.split(",")

    for line_spec in line_specs:
        if "-" in line_spec:
            # Handle line ranges (e.g., "1-10")
            start, end = map(int, line_spec.split("-"))
            selected_lines.extend(all_lines[start - 1 : end])
        else:
            # Handle single line numbers
            line_number = int(line_spec)
            if 1 <= line_number <= len(all_lines):
                selected_lines.append(all_lines[line_number - 1])

    return "".join(selected_lines)


def _extract_lines(embedded_line: str) -> str:
    to_expand_path_elements = re.search("{!>(.*)!}", embedded_line).group(1).strip()
    lines_spec = ""
    if "[ln:" in to_expand_path_elements:
        to_expand_path_elements, lines_spec = to_expand_path_elements.split("[ln:")
        to_expand_path_elements = to_expand_path_elements.strip()
        lines_spec = lines_spec[:-1]

    if Path("./docs/docs_src").exists():
        base_path = Path("./docs")
    elif Path("./docs_src").exists():
        base_path = Path("./")
    else:
        raise ValueError("Couldn't find docs_src directory")

    return _read_lines_from_file(base_path / to_expand_path_elements, lines_spec)


@app.command()
def expand_markdown(
    input_markdown_path: Annotated[Path, typer.Argument(...)],
    output_markdown_path: Annotated[Path, typer.Argument(...)],
) -> None:
    """Expand markdown files with embedded lines from other files.

    Args:
        input_markdown_path: The path of the markdown file to expand.
        output_markdown_path: The path of the expanded markdown file.

    """
    with (
        input_markdown_path.open() as input_file,
        output_markdown_path.open("w") as output_file,
    ):
        for line in input_file:
            # Check if the line does not contain the "{!>" pattern
            if "{!>" not in line:
                # Write the line to the output file
                output_file.write(line)
            else:
                output_file.write(_extract_lines(embedded_line=line))


def _remove_lines_between_dashes(file_path: Path) -> None:
    with file_path.open() as file:
        lines = file.readlines()

    start_dash_index = None
    end_dash_index = None
    new_lines = []

    for index, line in enumerate(lines):
        if line.strip() == "---":
            if start_dash_index is None:
                start_dash_index = index
            else:
                end_dash_index = index
                # Remove lines between the two dashes
                new_lines = (
                    lines[:start_dash_index] + new_lines + lines[end_dash_index + 1 :]
                )
                start_dash_index = end_dash_index = None
                break  # NOTE: Remove this line if you have multiple dash chunks

    with file_path.open("w") as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    app()
