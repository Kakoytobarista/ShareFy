import os
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, Response
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
LIVE_TIME_TOKEN = os.getenv("LIVE_TIME_TOKEN")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def create_access_token(user: UserModel, response: Response):
    expire = datetime.utcnow() + timedelta(minutes=int(LIVE_TIME_TOKEN))
    expire_utc = expire.replace(tzinfo=timezone.utc)
    user_copy = deepcopy(user)
    to_encode_data = {"exp": expire_utc, "sub": user_copy.email}
    encoded_jwt = jwt.encode(claims=to_encode_data, key=SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(key=TokenEnum.TOKEN_KEY.value, value=encoded_jwt, expires=expire_utc)

    return encoded_jwt


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
