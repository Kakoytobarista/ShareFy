from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.session import get_db
from data_managers.auth import AuthDataManager
from data_managers.user import UserDataManager
from enums import EndpointPath, TokenEnum
from schemas.v1.auth import CreateUserSchema, LoginSchema
from schemas.v1.token import TokenResponseSchema
from services.auth import AuthService

router = APIRouter(prefix="/auth")


class SendMailSuccessCreateAccError(Exception):
    pass


@router.post(EndpointPath.REGISTER.value, response_model=CreateUserSchema, status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserSchema, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(managers=[UserDataManager(session=session),
                                         AuthDataManager(session=session)])
    created_user = await auth_service.create_user(user)
    return created_user


@router.post(EndpointPath.LOGIN.value, response_model=TokenResponseSchema, status_code=status.HTTP_200_OK)
async def login(response: Response, login_data: LoginSchema, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(managers=[AuthDataManager(session=session),
                                         UserDataManager(session=session)])
    login_schema = await auth_service.login(login_data)
    response.set_cookie(
        key=TokenEnum.TOKEN_KEY.value, value=login_schema.access_token, expires=login_schema.expired_date, httponly=True)
    response.set_cookie(
        key=TokenEnum.REFRESH_TOKEN_KEY.value, value=login_schema.refresh_token, httponly=True)

    return login_schema
