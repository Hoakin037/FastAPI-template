from copy import deepcopy
from typing import Any

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo
from pydantic.json_schema import SkipJsonSchema


def partial_schema(model: type[BaseModel]):
    def make_field_optional(
        field: FieldInfo,
        default: Any = None,
    ) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = (
            (field.annotation | SkipJsonSchema[None])
            if field.annotation is not None
            else SkipJsonSchema[None]
        )

        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )
