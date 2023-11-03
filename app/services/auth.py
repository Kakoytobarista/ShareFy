from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.auth import UserModel
from app.schemas.auth import CreateUserSchema, LoginSchema, UserSchema
from app.services.base import BaseDataManager, BaseService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashingMixin:
    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class AuthService(HashingMixin, BaseService):
    def create_user(self, user: CreateUserSchema) -> UserSchema:
        user_model = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=self.bcrypt(user.password),
        )
        AuthDataManager(self.session).add_user(user_model)
        return UserSchema.from_orm(user_model)

    def login(self, login_data: LoginSchema, db: Session = Depends(get_db)) -> UserSchema:
        user = AuthDataManager(db).get_user_by_email(login_data.email)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        if not self.verify(user.hashed_password, login_data.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return UserSchema.from_orm(user)


class AuthDataManager(BaseDataManager):
    def add_user(self, user: UserModel) -> None:
        self.add_one(user)

    def get_user_by_email(self, email: str) -> UserModel:
        return self.query(UserModel).filter(UserModel.email == email).first()
