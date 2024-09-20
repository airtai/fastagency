import subprocess
from pathlib import Path

from create_api_docs import get_navigation_template


def _run_command_help(command: list[str]) -> str:
    """Run the CLI command with --help and capture the output."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


CLI_INTRO = """The **FastAgency Command Line Interface (CLI)** enables developers to manage and run FastAgency projects directly from the terminal.
The CLI simplifies interactions with FastAgency apps, providing options for running, testing, and managing workflows efficiently."""


def _format_md_file(command_description_and_parameters: str) -> str:
    command_description_and_parameters = command_description_and_parameters.strip()
    command = command_description_and_parameters.split("\n")[0]
    command_description_and_parameters = command_description_and_parameters.replace(
        command, ""
    ).strip()
    command = command.replace("Usage:", "").strip()

    if "╭─ " in command_description_and_parameters:
        description = command_description_and_parameters.split("╭─ ")[0].strip()
        parameters = command_description_and_parameters.replace(description, "").strip()
    else:
        description = command_description_and_parameters
        parameters = ""

    formated_content = f"""```

{command}

```

{description}

"""
    if parameters:
        formated_content += f"""
```

{parameters}

```
"""
    return formated_content


def _generate_cli_docs(
    cli_name: str, docs_path: Path, cli_dir: str = "user-guide/cli"
) -> str:
    """Generate CLI usage documentation for the main CLI and subcommands."""
    cli_help_output = _run_command_help([cli_name, "--help"])

    docs_path = docs_path / cli_dir

    # Save main CLI help output to a file
    main_help_file = docs_path / "fastagency-cli.md"
    formated_content = _format_md_file(cli_help_output)
    main_help_file.write_text(f"""# CLI

{CLI_INTRO}

{formated_content}""")

    # Define the subcommands you want to capture help for
    subcommands = ["run", "dev", "version"]

    cli_summary = f"({cli_dir}/fastagency-cli.md)"

    submodule = 2
    indent = " " * 4 * submodule
    # Generate and save documentation for each subcommand
    for subcommand in subcommands:
        command_description_and_parameters = _run_command_help(
            [cli_name, subcommand, "--help"]
        )

        formated_content = _format_md_file(command_description_and_parameters)

        file_name = f"fastagency-{subcommand}.md"
        subcommand_file = docs_path / file_name
        subcommand_file.write_text(formated_content)
        # Uppercase the first letter of the subcommand
        cli_summary += f"\n{indent}- [{subcommand.capitalize()}]({cli_dir}/{file_name})"

    return cli_summary


def create_cli_docs(
    root_path: Path,
    module: str,
    navigation_template: str,
) -> str:
    """Create CLI usage documentation for a module.

    Args:
        root_path: The root path of the project.
        module: The name of the module.
        navigation_template: The navigation template for the documentation.
    """
    docs_dir = root_path / "docs"

    # Generate CLI usage documentation
    cli = _generate_cli_docs(module, docs_dir / "en")

    summary = navigation_template.format(cli=cli, api="{api}")

    summary = "\n".join(filter(bool, (x.rstrip() for x in summary.split("\n"))))

    (docs_dir / "SUMMARY.md").write_text(summary)

    return summary


if __name__ == "__main__":
    root_path = Path(__file__).resolve().parent
    docs_dir = root_path / "docs"

    navigation_template = get_navigation_template(docs_dir)

    create_cli_docs(root_path, "fastagency", navigation_template)
