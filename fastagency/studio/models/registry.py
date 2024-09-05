from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
    Type,
)

from pydantic import BaseModel, Field

from .base import (
    M,
    Model,
    ObjectReference,
    create_reference_model,
)

__all__ = [
    "ModelSchema",
    "ModelSchemas",
    "Registry",
    "Schemas",
    "register",
]


class ModelSchema(BaseModel):
    name: Annotated[str, Field(description="The name of the item")]
    json_schema: Annotated[
        dict[str, Any], Field(description="The schema for the model")
    ]


class ModelSchemas(BaseModel):
    name: Annotated[str, Field(description="The name of the type of models")]
    schemas: Annotated[
        list[ModelSchema],
        Field(
            description="The schemas for all registred models of the particular types"
        ),
    ]


class Schemas(BaseModel):
    list_of_schemas: Annotated[
        list[ModelSchemas],
        Field(description="The list of schemas for all registred models"),
    ]


class Registry:
    def __init__(self) -> None:
        """Initialize the registry."""
        self._store: "Dict[str, Dict[str, Tuple[Optional[Type[Model]], Type[ObjectReference]]]]" = {}

    def register(self, type_name: str) -> Callable[[type[M]], type[M]]:
        if type_name not in self._store:
            self._store[type_name] = {}

        type_store = self._store[type_name]

        def _inner(model: type[M]) -> type[M]:
            model_type_name = model.__name__

            model_tuple = type_store.get(model_type_name)
            existing_model, existing_ref = model_tuple if model_tuple else (None, None)

            if existing_model:
                raise ValueError(
                    f"Model '{model_type_name}' already registered under '{type_name}'"
                )

            if existing_ref is None:
                reference_model: type[ObjectReference] = create_reference_model(
                    model, type_name=type_name
                )
            else:
                reference_model = existing_ref
                reference_model._data_class = model

            model._reference_model = reference_model

            type_store[model_type_name] = (model, reference_model)

            return model

        return _inner

    def get_model_type(self, type: str, name: str) -> type[Model]:
        if type not in self._store:
            raise ValueError(f"No models registered under '{type}'")

        models = self._store[type]
        if name not in models:
            raise ValueError(f"No model '{name}' registered under '{type}'")

        model, _ = models[name]
        if model is None:
            raise ValueError(f"Model '{name}' not found in '{type}'")

        return model

    def get_models_refs_by_type(self, type: str) -> list[type[ObjectReference]]:
        if type not in self._store:
            raise ValueError(f"No models registered under '{type}'")

        models = self._store[type]

        return [ref for _, ref in models.values()]

    def create_reference(
        self, type_name: str, model_name: str
    ) -> type[ObjectReference]:
        # check if the type_name is already registered
        if type_name not in self._store:
            self._store[type_name] = {}

        # check if the model_name is already registered
        if model_name in self._store[type_name]:
            raise ValueError("Reference already created for the model")

        # create a reference model and store it
        reference_model = create_reference_model(
            type_name=type_name, model_name=model_name
        )
        self._store[type_name][model_name] = (None, reference_model)

        return reference_model

    _default_registry: "Optional[Registry]" = None

    @classmethod
    def get_default(cls) -> "Registry":
        if cls._default_registry is None:
            cls._default_registry = cls()
        return cls._default_registry

    def get_dongling_references(self) -> list[type[ObjectReference]]:
        """Return a list of all dongling references."""
        return [
            reference
            for type_name, models in self._store.items()
            for model_name, (model, reference) in models.items()
            if model is None
        ]

    def get_model_schema(self, model: type[Model]) -> ModelSchema:
        """Return the schema for the given model."""
        return ModelSchema(
            name=model.__name__,
            json_schema=model.model_json_schema(),
        )

    def get_model_schemas(self, type_name: str) -> ModelSchemas:
        """Return the schemas for all models of the given type."""
        models = self._store.get(type_name)
        if models is None:
            raise ValueError(f"No models registered under '{type_name}'")

        schemas = [
            self.get_model_schema(model)  # type: ignore[arg-type]
            for _, (model, _) in models.items()
        ]

        return ModelSchemas(name=type_name, schemas=schemas)

    def get_schemas(self) -> Schemas:
        """Return the schemas for all registered models."""
        dongling_references = self.get_dongling_references()
        if dongling_references:
            raise ValueError(
                f"Found {len(dongling_references)} dongling references: {dongling_references}"
            )

        list_of_schemas = [
            self.get_model_schemas(type_name) for type_name in self._store
        ]

        return Schemas(list_of_schemas=list_of_schemas)

    def validate(self, type: str, name: str, model: dict[str, Any]) -> Model:
        model_type = self.get_model_type(type, name)
        return model_type(**model)


def register(type_name: str) -> Callable[[type[M]], type[M]]:
    return Registry.get_default().register(type_name)
