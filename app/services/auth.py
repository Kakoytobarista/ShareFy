from http import HTTPStatus
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.backend.session import get_db
from app.enums import ErrorEnum
from app.models.v1.auth import AuthUserModel
from app.schemas.v1.auth import CreateUserSchema, LoginSchema
from app.services.base import BaseDataManager, BaseService
from app.utils.auth import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashingMixin:
    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class AuthService(HashingMixin, BaseService):
    def create_user(self, user: CreateUserSchema, db: Session):
        existing_user = AuthDataManager(session=db).get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=ErrorEnum.EMAIL_ALREADY_EXIST.value)

        existing_user = AuthDataManager(session=db).get_user_by_login(user.login)
        if existing_user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=ErrorEnum.LOGIN_ALREADY_EXIST.value)

        user_model = AuthUserModel(
            login=user.login,
            email=user.email,
            hashed_password=self.bcrypt(user.hashed_password),
        )
        AuthDataManager(session=db).add_user(user=user_model)
        return CreateUserSchema(login=user_model.login,
                                email=user_model.email,
                                hashed_password=user_model.hashed_password,
                                date_of_create=user_model.date_of_create)

    def login(self, login_data: LoginSchema, db: Session) -> dict:
        user = AuthDataManager(session=db).get_user_by_email(email=login_data.email)
        if not user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorEnum.USER_NOT_FOUND)
        if not self.verify(user.hashed_password, login_data.password):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorEnum.INCORRECT_PASSWORD)

        access_token = create_access_token(data={"sub": user.id})
        return {"access_token": access_token, "token_type": "bearer"}


class AuthDataManager(BaseDataManager):
    def add_user(self, user: AuthUserModel) -> None:
        self.add_one(user)

    def get_user_by_email(self, email: str) -> AuthUserModel:
        return self.get_one(AuthUserModel, email=email)

    def get_user_by_login(self, login) -> AuthUserModel:
        return self.get_one(AuthUserModel, login=login)
