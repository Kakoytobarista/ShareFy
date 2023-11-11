from http import HTTPStatus

from passlib.context import CryptContext
from fastapi import HTTPException

from app.enums import ErrorEnum
from app.models.v1.user import UserModel
from app.schemas.v1.auth import CreateUserSchema, LoginSchema
from app.schemas.v1.token import TokenResponseSchema
from app.services.base import BaseService
from app.utils.token import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashingMixin:
    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class AuthService(HashingMixin, BaseService):
    def __init__(self, managers):
        super().__init__(managers=managers)

    async def create_user(self, user: CreateUserSchema) -> CreateUserSchema:
        existing_user = await self.manager.get_user_by_email(email=user.email)
        if existing_user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=ErrorEnum.EMAIL_ALREADY_EXIST.value)

        existing_user = await self.manager.get_user_by_login(login=user.login)
        if existing_user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=ErrorEnum.LOGIN_ALREADY_EXIST.value)

        user_model = UserModel(
            login=user.login,
            email=user.email,
            hashed_password=self.bcrypt(user.hashed_password),
            first_name=user.first_name,
            last_name=user.last_name,
            date_of_birth=user.date_of_birth,
            person_type=user.person_type,
            is_active=user.is_active
        )

        await self.manager.create(model=user_model)
        saved_user = await self.manager.get_user_by_login(login=user.login)
        user_schema = CreateUserSchema(
            login=saved_user.login,
            email=saved_user.email,
            hashed_password="Hidden",
            date_of_create=saved_user.date_of_create,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            person_type=saved_user.person_type,
            is_active=saved_user.is_active
        )
        return user_schema

    async def login(self, login_data: LoginSchema) -> TokenResponseSchema:
        user = await self.manager.get_user_by_email(email=login_data.email)
        if not user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorEnum.USER_NOT_FOUND.value)
        if not self.verify(user.hashed_password, login_data.hashed_password):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorEnum.INCORRECT_PASSWORD.value)

        access_token = await create_access_token(user=user)
        return TokenResponseSchema(access_token=access_token, token_type="bearer")
