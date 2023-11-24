from datetime import datetime

from pydantic import BaseModel


class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str
    expired_date: datetime


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class AccessRefreshTokenSchema(BaseModel):
    access_token: AccessTokenSchema
    refresh_token: RefreshTokenSchema
