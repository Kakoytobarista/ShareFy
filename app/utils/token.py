import os
from datetime import datetime, timedelta
from typing import Annotated
from copy import deepcopy


from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.backend.session import get_db
from app.data_managers.user import UserDataManager
from app.enums import ErrorEnum
from app.models.v1.user import UserModel

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
LIVE_TIME_TOKEN = os.getenv("LIVE_TIME_TOKEN")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def create_access_token(user: UserModel):
    expire = datetime.utcnow() + timedelta(minutes=int(LIVE_TIME_TOKEN))
    user_copy = deepcopy(user)
    to_encode_data = {"exp": expire, "sub": user_copy.login}
    encoded_jwt = jwt.encode(claims=to_encode_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: AsyncSession = Depends(get_db)):
    try:
        print("JHELLO")
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")
        if login is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorEnum.INVALID_TOKEN.value)

        user = UserDataManager(session=db_session).get_user_by_login(login=login)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorEnum.USER_NOT_FOUND.value)

        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorEnum.INVALID_TOKEN.value)
