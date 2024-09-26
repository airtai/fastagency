import pytest
from typer.testing import CliRunner

from fastagency.cli import app
from tests.conftest import InputMock

runner = CliRunner()

INPUT_MESSAGE = "Today's theme is Leonardo da Vinci"


@pytest.mark.openai
@pytest.mark.xfail(strict=False)
def test_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "builtins.input",
        InputMock(
            [
                INPUT_MESSAGE,
                "1) Mona Lisa 2) Vitruvian Man 3) Florence at the time of Leonardo",
                "B",
            ]
        ),
    )

    result = runner.invoke(
        app,
        [
            "run",
            "docs/docs_src/user_guide/custom_user_interactions/main.py",
            "--single-run",
        ],
    )
    assert result.exit_code == 0
    assert INPUT_MESSAGE in result.stdout
    assert "retrieve_exam_questions" in result.stdout
