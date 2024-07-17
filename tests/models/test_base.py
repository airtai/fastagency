import uuid

import pytest
from pydantic import BaseModel

from fastagency.models.base import (
    Model,
    create_reference_model,
    get_reference_model,
)


def test_create_reference_model() -> None:
    class MyModel(Model):
        i: int
        s: str

    MyModelRef = create_reference_model(MyModel, type_name="my_type")  # noqa: N806

    assert hasattr(MyModelRef, "get_data_model")
    data_model = MyModelRef.get_data_model()
    assert data_model == MyModel

    schema = MyModelRef.model_json_schema()
    expected = {
        "properties": {
            "type": {
                "const": "my_type",
                "default": "my_type",
                "description": "The name of the type of the data",
                "enum": ["my_type"],
                "title": "Type",
                "type": "string",
            },
            "name": {
                "const": "MyModel",
                "default": "MyModel",
                "description": "The name of the data",
                "enum": ["MyModel"],
                "title": "Name",
                "type": "string",
            },
            "uuid": {
                "description": "The unique identifier",
                "format": "uuid",
                "title": "UUID",
                "type": "string",
            },
        },
        "required": ["uuid"],
        "title": "MyModelRef",
        "type": "object",
    }
    assert schema == expected

    my_uuid = uuid.uuid4()
    o = MyModelRef.create(uuid=my_uuid)
    dump = o.model_dump()
    assert dump == {"type": "my_type", "name": "MyModel", "uuid": my_uuid}

    loaded = MyModelRef(**dump)
    assert loaded == o


def test_get_reference_model() -> None:
    class MyModel(Model):
        i: int
        s: str

    MyModelRef = create_reference_model(MyModel, type_name="my_type")  # noqa: N806

    assert get_reference_model(MyModel) == MyModelRef
    assert get_reference_model(MyModelRef) == MyModelRef
    with pytest.raises(
        ValueError, match="Class 'BaseModel' is not and does not have a reference"
    ):
        get_reference_model(BaseModel)
