import tempfile
from pathlib import Path

import pytest
from datamodel_code_generator import DataModelType
from fastapi_code_generator.__main__ import generate_code
from fastapi_code_generator.parser import OpenAPIParser

from fastagency.api.openapi.patch_datamodel_code_generator import (
    original_apply_discriminator_type,
)

OPENAPI_FILE_PATHS = Path(__file__).parent
TEMPLATE_DIR = Path(__file__).parents[4] / "templates"

assert TEMPLATE_DIR.exists(), TEMPLATE_DIR


def test_datamodel_codegen_discriminator_stale_patch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """This test checks if a RuntimeError is raised due to a discriminator containing additional fields in the properties.

    If this error is not raised, it indicates that the original issue has been resolved,
    meaning the patch `patch_apply_discriminator_type` applied in
    `fastagency/api/openapi/__init__.py` is likely stale and can be removed.
    """
    monkeypatch.setattr(
        OpenAPIParser,
        "_Parser__apply_discriminator_type",
        original_apply_discriminator_type,
    )

    discriminator_with_properties_spec_path = (
        OPENAPI_FILE_PATHS / "discriminator_in_root_with_properties.json"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        td = Path(temp_dir)

        # Expecting RuntimeError if patch is still required; if not, the patch may be obsolete.
        with pytest.raises(
            RuntimeError,
            match="Discriminator type is not found.",
        ):
            generate_code(
                input_name=discriminator_with_properties_spec_path.name,
                input_text=discriminator_with_properties_spec_path.read_text(),
                encoding="utf-8",
                output_dir=td,
                template_dir=TEMPLATE_DIR,
                output_model_type=DataModelType.PydanticV2BaseModel,
                custom_visitors=[
                    Path(__file__).parents[4]
                    / "fastagency"
                    / "api"
                    / "openapi"
                    / "security_schema_visitor.py"
                ],
            )
