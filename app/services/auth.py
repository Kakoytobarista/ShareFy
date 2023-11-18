from http import HTTPStatus

from fastapi import HTTPException, Response
from passlib.context import CryptContext

from enums import ErrorEnum
from models.v1.user import UserModel
from schemas.v1.auth import CreateUserSchema, LoginSchema
from schemas.v1.token import TokenResponseSchema
from services.base import BaseService
from utils.token import create_access_token

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

        user_model = UserModel(
            email=user.email,
            hashed_password=self.bcrypt(user.hashed_password)
        )

        await self.manager.create(model=user_model)
        saved_user = await self.manager.get_user_by_email(email=user.email)
        user_schema = CreateUserSchema(
            email=saved_user.email,
            hashed_password="Hidden"
        )
        return user_schema

    async def login(self, response: Response, login_data: LoginSchema) -> TokenResponseSchema:
        user = await self.manager.get_user_by_email(email=login_data.email)
        if not user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorEnum.USER_NOT_FOUND.value)
        if not self.verify(user.hashed_password, login_data.hashed_password):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorEnum.INCORRECT_PASSWORD.value)

        access_token = await create_access_token(user=user, response=response)
        return TokenResponseSchema(access_token=access_token, token_type="bearer")
