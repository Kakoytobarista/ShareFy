from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.session import get_db
from app.data_managers.auth import AuthDataManager
from app.data_managers.user import UserDataManager
from app.enums import EndpointPath
from app.schemas.v1.auth import CreateUserSchema, LoginSchema
from app.schemas.v1.token import TokenResponseSchema
from app.services.auth import AuthService

router = APIRouter(prefix="/auth")


class SendMailSuccessCreateAccError(Exception):
    pass


@router.post(EndpointPath.REGISTER.value, response_model=CreateUserSchema, status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserSchema, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(managers=[UserDataManager(session=session),
                                         AuthDataManager(session=session)])
    created_user = await auth_service.create_user(user)
    # await send_email_async() HERE WILL EMAIL SEND EVENT
    return created_user


@router.post(EndpointPath.LOGIN.value, response_model=TokenResponseSchema, status_code=status.HTTP_200_OK)
async def login(login_data: LoginSchema, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(managers=[UserDataManager(session=session),
                                         AuthDataManager(session=session)])
    access_token = await auth_service.login(login_data)
    return access_token
