import os
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from data_managers.user import UserDataManager
from database.session import get_db
from dotenv import load_dotenv
from enums import ErrorEnum, TokenEnum
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.v1.user import UserModel
from schemas.v1.token import AccessTokenSchema, RefreshTokenSchema
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
LIVE_TIME_TOKEN = os.getenv("LIVE_TIME_TOKEN")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenManager:
    def __init__(self):
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
        self.LIVE_TIME_TOKEN = os.getenv("LIVE_TIME_TOKEN")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def generate_refresh_token(self, user_data: UserModel) -> RefreshTokenSchema:
        expire = datetime.utcnow() + timedelta(minutes=int(self.LIVE_TIME_TOKEN))
        expire_utc = expire.replace(tzinfo=timezone.utc)
        user_copy = deepcopy(user_data)
        to_encode_data = {"exp": expire_utc, "sub": user_copy.email}
        encoded_refresh_token = jwt.encode(claims=to_encode_data, key=self.SECRET_KEY_REFRESH, algorithm=self.ALGORITHM)
        return RefreshTokenSchema(refresh_token=encoded_refresh_token)

    @staticmethod
    async def get_refresh_token_from_store(request: Request) -> str:
        refresh_token = request.cookies.get(TokenEnum.REFRESH_TOKEN_KEY.value)
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorEnum.INVALID_REFRESH_TOKEN.value)
        return refresh_token

    async def generate_access_token(self, user_data: UserModel) -> AccessTokenSchema:
        expire = datetime.utcnow() + timedelta(minutes=int(self.LIVE_TIME_TOKEN))
        expire_utc = expire.replace(tzinfo=timezone.utc)
        user_copy = deepcopy(user_data)
        to_encode_data = {"exp": expire_utc, "sub": user_copy.email}
        access_token = jwt.encode(claims=to_encode_data, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
        return AccessTokenSchema(access_token=access_token, token_type=TokenEnum.TOKEN_KEY.value,
                                 expired_date=expire_utc)

    async def decode_refresh_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY_REFRESH, algorithms=[self.ALGORITHM])
            return payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorEnum.INVALID_REFRESH_TOKEN.value)


class TokenService:
    def __init__(self, manager: TokenManager = TokenManager()):
        self.manager = manager

    async def get_access_token(self, user_data) -> AccessTokenSchema:
        return await self.manager.generate_access_token(user_data=user_data)

    def get_refresh_token(self, user_data):
        return self.manager.generate_refresh_token(user_data=user_data)


async def get_current_user(request: Request, db_session: AsyncSession = Depends(get_db)):
    try:
        token = request.cookies.get(TokenEnum.TOKEN_KEY.value)
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorEnum.INVALID_TOKEN.value)

        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = await UserDataManager(session=db_session).get_user_by_email(email=email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorEnum.USER_NOT_FOUND.value)

        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorEnum.INVALID_TOKEN.value)
