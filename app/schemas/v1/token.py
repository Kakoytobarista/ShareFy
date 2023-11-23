from datetime import datetime


from pydantic import BaseModel


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expired_date: datetime
