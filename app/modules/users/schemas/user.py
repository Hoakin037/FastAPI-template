from uuid import UUID

from pydantic import Field

from app.shared.schemas import CoreSchema
from app.shared.utils import partial_schema


class UserCreate(CoreSchema):
    name: str = Field(max_length=72)
    surname: str = Field(max_length=72)
    age: int = Field(gt=0, lt=100)


@partial_schema
class UserUpdate(UserCreate):
    pass


class User(CoreSchema):
    sid: UUID
    name: str
    surname: str
    age: int
