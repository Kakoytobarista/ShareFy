from pydantic import BaseModel
from enum import Enum as PydanticEnum
from datetime import datetime


class PersonType(str, PydanticEnum):
    regular = "regular"
    moderator = "moderator"
    admin = "admin"


class AuthUserSchema(BaseModel):
    id: int
    login: str
    hashed_password: str
    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    person_type: PersonType
    date_of_create: datetime


class CreateUserSchema(BaseModel):
    login: str
    email: str
    hashed_password: str
    date_of_create: datetime = None


class LoginSchema(BaseModel):
    email: str
    hashed_password: str
