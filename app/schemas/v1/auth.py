from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    login: str
    email: str
    hashed_password: str
    date_of_create: datetime = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    person_type: str = 'regular'
    date_of_birth: datetime = None
    is_active: bool = True


class LoginSchema(BaseModel):
    email: str
    hashed_password: str
