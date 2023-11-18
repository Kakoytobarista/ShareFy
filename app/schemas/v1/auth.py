from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    email: str
    hashed_password: str


class LoginSchema(BaseModel):
    email: str
    hashed_password: str
