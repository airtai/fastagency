import pytest

from fastagency.helpers import create_autogen, get_model_by_ref
from fastagency.models.base import Model, ObjectReference

from ...helpers import get_by_tag, parametrize_fixtures


class TestLLMKeys:
    @pytest.mark.asyncio()
    @pytest.mark.db()
    @pytest.mark.llm()
    @parametrize_fixtures("llm_key_ref", get_by_tag("llm-key"))
    async def test_llm_key_constructor(
        self,
        llm_key_ref: ObjectReference,
    ) -> None:
        model = await get_model_by_ref(llm_key_ref)
        assert isinstance(model, Model)

    @pytest.mark.asyncio()
    @pytest.mark.db()
    @pytest.mark.llm()
    @parametrize_fixtures("llm_key_ref", get_by_tag("llm-key"))
    async def test_llm_key_create_autogen(
        self,
        user_uuid: str,
        llm_key_ref: ObjectReference,
    ) -> None:
        # Call create_autogen
        actual_api_key = await create_autogen(
            model_ref=llm_key_ref,
            user_uuid=user_uuid,
        )
        assert isinstance(actual_api_key, str)
