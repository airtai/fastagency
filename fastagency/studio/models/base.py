from abc import ABC, abstractmethod
from typing import (
    Annotated,
    Any,
    Literal,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
)
from uuid import UUID

from pydantic import BaseModel, create_model, model_validator
from pydantic import Field as PydanticField
from typing_extensions import TypeAlias

from ..db.base import DefaultDB

M = TypeVar("M", bound="Model")

__all__ = [
    "ObjectReference",
    "create_reference_model",
    "get_reference_model",
    "Model",
    "Field",
]


T = TypeVar("T", bound="Model")


# abstract class
class Model(BaseModel, ABC):
    name: Annotated[
        str, PydanticField(..., description="The name of the item", min_length=1)
    ]
    _reference_model: "Optional[Type[ObjectReference]]" = None

    @classmethod
    def get_reference_model(cls) -> "Type[ObjectReference]":
        if cls._reference_model is None:
            raise ValueError("reference model not set")
        return cls._reference_model

    @classmethod
    @abstractmethod
    async def create_autogen(
        cls, model_id: UUID, user_id: UUID, **kwargs: Any
    ) -> Any: ...  # pragma: no cover

    @classmethod
    async def from_db(cls: type[T], model_id: UUID) -> T:
        my_model_dict = await DefaultDB.backend().find_model(model_id)
        my_model = cls(**my_model_dict["json_str"])

        return my_model


class ObjectReference(BaseModel):
    type: Annotated[
        str, PydanticField(description="The name of the type of the data")
    ] = ""
    name: Annotated[str, PydanticField(description="The name of the data")] = ""
    uuid: Annotated[UUID, PydanticField(description="The unique identifier")]

    _data_class: Optional["Type[Model]"] = None

    @model_validator(mode="after")
    def check_type(self) -> "ObjectReference":
        if self.type == "" or self.name == "":
            raise ValueError("type and name must be set")
        return self

    @classmethod
    def get_data_model(cls) -> "Type[Model]":
        """Get the data class for the reference.

        This method returns the data class that is associated with the reference class.

        Returns:
            Type[BM]: The data class for the reference

        Raises:
            ValueError: If the data class is not set

        """
        if cls._data_class is None:
            raise RuntimeError("data class not set")

        return cls._data_class

    @classmethod
    def create(cls, uuid: UUID) -> "ObjectReference":
        """Factory method to create a new instance of the class.

        This method is used to create a new instance of the class with the given UUID. It
        is exactly the same as calling `ObjectReference(uuid=uuid)`, but without type
        checking failing because of the missing `type` and `name` arguments.

        Args:
            uuid (UUID): The unique identifier of the object

        Returns:
            ObjectReference: The new instance of the class
        """
        return cls(uuid=uuid)  # type: ignore[call-arg]


def create_reference_model(
    model_class: Optional[type[M]] = None,
    *,
    type_name: str,
    model_name: Optional[str] = None,
) -> type[ObjectReference]:
    if model_class is None and model_name is None:
        raise ValueError("Either model_class or model_name should be provided")
    if model_class is not None and model_name is not None:
        raise ValueError("Only one of model_class or model_name should be provided")

    model_type_name = model_class.__name__ if model_class is not None else model_name

    LiteralType: TypeAlias = Literal[type_name]  # type: ignore[valid-type]
    LiteralModelName: TypeAlias = Literal[model_type_name]  # type: ignore[valid-type]

    reference_model = create_model(
        f"{model_type_name}Ref",
        type=(
            Annotated[  # type: ignore[valid-type]
                LiteralType,
                PydanticField(description="The name of the type of the data"),
            ],
            type_name,
        ),
        name=(
            Annotated[
                LiteralModelName, PydanticField(description="The name of the data")
            ],
            model_type_name,
        ),
        uuid=(
            Annotated[
                UUID, PydanticField(description="The unique identifier", title="UUID")
            ],
            ...,
        ),
        __base__=ObjectReference,
    )
    reference_model.__module__ = (
        f"fastagency.studio.models.{type_name}.{model_type_name}._generated"
    )

    reference_model._data_class = model_class  # type: ignore[attr-defined]
    if model_class is not None:
        model_class._reference_model = reference_model

    return reference_model  # type: ignore[return-value]


class ModelTypeFinder(Protocol):
    def get_model_type(self, type: str, name: str) -> type[Model]: ...


def get_reference_model(model: type[BaseModel]) -> type[ObjectReference]:
    if issubclass(model, ObjectReference):
        return model
    elif hasattr(model, "_reference_model"):
        return model._reference_model  # type: ignore[attr-defined,no-any-return]
    raise ValueError(f"Class '{model.__name__}' is not and does not have a reference")


def Field(  # noqa: N802
    default: Any = ...,
    *,
    description: Optional[str] = None,
    tooltip_message: Optional[str] = None,
    immutable_after_creation: bool = False,
    **kwargs: Any,
) -> Any:
    metadata: dict[str, Union[str, bool]] = {}

    if tooltip_message is not None:
        metadata["tooltip_message"] = tooltip_message
    if immutable_after_creation:
        metadata["immutable_after_creation"] = immutable_after_creation

    # Create json_schema_extra only if we have metadata
    if metadata:
        kwargs["json_schema_extra"] = {"metadata": metadata}

    return PydanticField(  # type: ignore[pydantic-field]
        default, description=description, **kwargs
    )
