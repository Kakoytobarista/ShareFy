from datetime import datetime

from enums import PersonTypeEnum
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None
    person_type: PersonTypeEnum = PersonTypeEnum.REGULAR
    date_of_create: datetime = None
    is_active: bool | int = None


class DeactivateSchema(BaseModel):
    id: int
    is_active: bool | int = 0


class PersonTypeSchema(BaseModel):
    id: int
    person_type: PersonTypeEnum = "regular"
