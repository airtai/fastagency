import pytest

from fastagency.studio.models.base import Model
from fastagency.studio.models.registry import ModelSchema, Registry


class TestRegistry:
    def test_create_reference_success(self) -> None:
        registry = Registry()

        MySecretRef = registry.create_reference(  # noqa: N806
            type_name="my_secret", model_name="MySecret"
        )

        assert hasattr(MySecretRef, "get_data_model")
        with pytest.raises(RuntimeError, match="data class not set"):
            MySecretRef.get_data_model()
        assert registry._store["my_secret"]["MySecret"] == (None, MySecretRef)

    def test_create_reference_fail(self) -> None:
        registry = Registry()

        @registry.register("my_secret")
        class MySecret(Model):
            key: str

        with pytest.raises(ValueError, match="Reference already created for the model"):
            registry.create_reference(type_name="my_secret", model_name="MySecret")

    def test_register_simple_success(self) -> None:
        registry = Registry()

        @registry.register("my_type")
        class MyModel(Model):
            i: int
            s: str

        MyModelRef = MyModel.get_reference_model()  # noqa: N806
        assert registry._store["my_type"]["MyModel"] == (MyModel, MyModelRef)

    def test_register_complex_with_ref_success(self) -> None:
        registry = Registry()

        MySecretRef = registry.create_reference(  # noqa: N806
            type_name="my_secret", model_name="MySecret"
        )

        @registry.register("my_type")
        class MyModel(Model):
            i: int
            s: str
            secret: MySecretRef  # type: ignore[valid-type]

        MyModelRef = MyModel.get_reference_model()  # noqa: N806
        assert registry._store["my_type"]["MyModel"] == (MyModel, MyModelRef)

    def test_register_complex_with_nested_model_success(self) -> None:
        registry = Registry()

        @registry.register("my_secret")
        class MySecret(Model):
            key: str

        MySecretRef = MySecret.get_reference_model()  # noqa: N806

        @registry.register("my_type")
        class MyModel(Model):
            i: int
            s: str
            secret: MySecretRef  # type: ignore[valid-type]

        MyModelRef = MyModel.get_reference_model()  # noqa: N806
        assert registry._store["my_type"]["MyModel"] == (MyModel, MyModelRef)

    def test_get_default(self) -> None:
        registry = Registry.get_default()
        assert isinstance(registry, Registry)
        assert Registry.get_default() == registry

    def test_get_dongling_references(self) -> None:
        registry = Registry()

        assert registry.get_dongling_references() == []

        MySecretRef = registry.create_reference(  # noqa: N806
            type_name="my_secret", model_name="MySecret"
        )
        assert registry.get_dongling_references() == [MySecretRef]

        @registry.register("my_secret")
        class MySecret(Model):
            key: str

        assert registry.get_dongling_references() == []

    def test_get_model_schema_simple(self) -> None:
        registry = Registry()

        @registry.register("my_type")
        class MyModel(Model):
            i: int
            s: str

        schema = registry.get_model_schema(MyModel)  # type: ignore[type-abstract]
        expected = ModelSchema(
            name="MyModel",
            json_schema={
                "properties": {
                    "name": {
                        "description": "The name of the item",
                        "minLength": 1,
                        "title": "Name",
                        "type": "string",
                    },
                    "i": {"title": "I", "type": "integer"},
                    "s": {"title": "S", "type": "string"},
                },
                "required": ["name", "i", "s"],
                "title": "MyModel",
                "type": "object",
            },
        )
        assert schema == expected

    def test_get_model_schema_nested(self) -> None:
        registry = Registry()

        @registry.register("my_secret")
        class MySecret(Model):
            key: str

        MySecretRef = MySecret.get_reference_model()  # noqa: N806

        @registry.register("my_type")
        class MyModel(Model):
            i: int
            s: str
            secret: MySecretRef  # type: ignore[valid-type]

        schema = registry.get_model_schema(MyModel)  # type: ignore[type-abstract]
        expected = ModelSchema(
            name="MyModel",
            json_schema={
                "$defs": {
                    "MySecretRef": {
                        "properties": {
                            "type": {
                                "const": "my_secret",
                                "default": "my_secret",
                                "description": "The name of the type of the data",
                                "enum": ["my_secret"],
                                "title": "Type",
                                "type": "string",
                            },
                            "name": {
                                "const": "MySecret",
                                "default": "MySecret",
                                "description": "The name of the data",
                                "enum": ["MySecret"],
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
                        "title": "MySecretRef",
                        "type": "object",
                    }
                },
                "properties": {
                    "name": {
                        "description": "The name of the item",
                        "minLength": 1,
                        "title": "Name",
                        "type": "string",
                    },
                    "i": {"title": "I", "type": "integer"},
                    "s": {"title": "S", "type": "string"},
                    "secret": {"$ref": "#/$defs/MySecretRef"},
                },
                "required": ["name", "i", "s", "secret"],
                "title": "MyModel",
                "type": "object",
            },
        )
        assert schema == expected

    def test_get_model_schemas_simple(self) -> None:
        registry = Registry()

        @registry.register("my_type")
        class MyModel(Model):
            i: int
            s: str

        schemas = registry.get_model_schemas("my_type")
        assert len(schemas.schemas) == 1
        assert schemas.schemas[0].name == "MyModel"

    def test_get_schemas_simple(self) -> None:
        registry = Registry()

        @registry.register("my_type")
        class MyModel(Model):
            i: int
            s: str

        schemas = registry.get_schemas()
        assert len(schemas.list_of_schemas) == 1
        assert len(schemas.list_of_schemas[0].schemas) == 1
        assert schemas.list_of_schemas[0].schemas[0].name == "MyModel"

    def test_get_models_refs_by_type(self) -> None:
        registry = Registry()

        @registry.register("my_secret")
        class MySecretOne(Model):
            key: str

        MySecretTwoRef = registry.create_reference(  # noqa: N806
            type_name="my_secret", model_name="MySecretTwo"
        )

        refs = registry.get_models_refs_by_type("my_secret")
        assert set(refs) == {MySecretOne.get_reference_model(), MySecretTwoRef}
