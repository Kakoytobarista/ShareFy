from pydantic import BaseModel
from datetime import datetime
from enum import Enum as PydanticEnum


class PersonType(str, PydanticEnum):
    regular = "regular"
    moderator = "moderator"
    admin = "admin"


class UserSchema(BaseModel):
    id: int
    login: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None
    person_type: PersonType = "regular"
    date_of_create: datetime = None
    is_active: bool | int = None

