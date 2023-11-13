from pydantic import BaseModel
from datetime import datetime
from enum import Enum as PydanticEnum


class PersonType(str, PydanticEnum):
    regular = "regular"
    moderator = "moderator"
    admin = "admin"


class UserSchema(BaseModel):
    id: int
    email: str = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None
    person_type: PersonType = "regular"
    date_of_create: datetime = None
    is_active: bool | int = None


class DeactivateSchema(BaseModel):
    id: int
    is_active: bool | int = 0


class PersonTypeSchema(BaseModel):
    id: int
    person_type: PersonType = "regular"
