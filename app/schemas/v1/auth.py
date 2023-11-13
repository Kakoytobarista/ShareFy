from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    email: str
    hashed_password: str
    date_of_create: datetime = None
    person_type: str = 'regular'
    is_active: bool = True


class LoginSchema(BaseModel):
    email: str
    hashed_password: str
