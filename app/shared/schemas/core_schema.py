from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class CoreSchema(BaseModel):
    @field_validator("*", mode="after")
    def timezone_validate(cls, value: Any) -> Any:
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=UTC)

            value = value.replace(microsecond=0)

        return value

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
        json_encoders={datetime: lambda v: v.isoformat()},
    )
