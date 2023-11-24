from data_managers.auth import AuthDataManager
from data_managers.user import UserDataManager
from database.session import get_db
from enums import EndpointPath, TokenEnum
from fastapi import APIRouter, Depends, Response
from schemas.v1.auth import CreateUserSchema, LoginSchema
from schemas.v1.token import AccessTokenSchema
from services.auth import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from utils.token import TokenManager, TokenService

router = APIRouter(prefix="/auth")


class SendMailSuccessCreateAccError(Exception):
    pass


@router.post(EndpointPath.REGISTER.value, response_model=CreateUserSchema, status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserSchema, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(managers=[UserDataManager(session=session),
                                         AuthDataManager(session=session)])
    created_user = await auth_service.create_user(user)
    return created_user


@router.post(EndpointPath.LOGIN.value, response_model=AccessTokenSchema, status_code=status.HTTP_200_OK)
async def login(response: Response, login_data: LoginSchema, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(managers=[AuthDataManager(session=session),
                                         UserDataManager(session=session)])
    token_service = TokenService(manager=TokenManager())

    user = await auth_service.login(login_data)
    access_token = await token_service.get_access_token(user_data=user)
    refresh_token = await token_service.get_refresh_token(user_data=user)
    response.set_cookie(
        key=TokenEnum.TOKEN_KEY.value, value=access_token.access_token,
        expires=access_token.expired_date, httponly=True)
    response.set_cookie(
        key=TokenEnum.REFRESH_TOKEN_KEY.value, value=refresh_token.refresh_token, httponly=True)

    return access_token
