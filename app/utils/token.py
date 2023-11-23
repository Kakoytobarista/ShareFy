import os
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from typing import Tuple

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.session import get_db
from data_managers.user import UserDataManager
from enums import ErrorEnum, TokenEnum
from models.v1.user import UserModel

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
LIVE_TIME_TOKEN = os.getenv("LIVE_TIME_TOKEN")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def generate_refresh_token(user_data):
    expire = datetime.utcnow() + timedelta(minutes=int(LIVE_TIME_TOKEN))
    expire_utc = expire.replace(tzinfo=timezone.utc)
    user_copy = deepcopy(user_data)
    to_encode_data = {"exp": expire_utc, "sub": user_copy.email}
    encoded_refresh_token = jwt.encode(claims=to_encode_data, key=SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    print(f"NEW ENCODED REFRESH TOKEN{encoded_refresh_token}")
    return encoded_refresh_token


async def get_refresh_token(request: Request):
    refresh_token = request.cookies.get(TokenEnum.REFRESH_TOKEN_KEY.value)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorEnum.INVALID_REFRESH_TOKEN.value)
    return refresh_token


async def generate_access_token(user_data: UserModel) -> Tuple:
    expire = datetime.utcnow() + timedelta(minutes=int(LIVE_TIME_TOKEN))
    expire_utc = expire.replace(tzinfo=timezone.utc)
    user_copy = deepcopy(user_data)
    to_encode_data = {"exp": expire_utc, "sub": user_copy.email}
    encoded_jwt_token = jwt.encode(claims=to_encode_data, key=SECRET_KEY, algorithm=ALGORITHM)
    print(f"ACESS_TOKEN: {encoded_jwt_token}")
    return TokenEnum.TOKEN_KEY.value, encoded_jwt_token, expire_utc


def decode_refresh_token(refresh_token: str):
    try:
        print("IM IN DECODER")
        payload = jwt.decode(refresh_token, SECRET_KEY_REFRESH, algorithms=[ALGORITHM])
        print(f"PAYLOAD: {payload}")
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorEnum.INVALID_REFRESH_TOKEN.value)


async def get_current_user(request: Request, db_session: AsyncSession = Depends(get_db)):
    try:
        token = request.cookies.get(TokenEnum.TOKEN_KEY.value)
        print(token)
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
