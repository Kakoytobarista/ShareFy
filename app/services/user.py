from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enums import ErrorEnum
from app.models.v1.user import UserModel
from app.schemas.v1.user import UserSchema, DeactivateSchema
from app.services.base import BaseDataManager, BaseService


class UserService(BaseService):

    @staticmethod
    def get_user(user: UserSchema, session: Session) -> UserSchema:
        return UserDataManager(session=session).get_user_by_id(user_id=user.id)

    @staticmethod
    def get_all_users(session: Session) -> UserSchema:
        return UserDataManager(session=session).get_all_users()

    @staticmethod
    def get_active_users(session: Session) -> UserSchema:
        return UserDataManager(session=session).get_active_users()

    @staticmethod
    def deactivate_user(user: DeactivateSchema, session: Session):
        user_data_manager = UserDataManager(session=session)
        user: UserModel = user_data_manager.get_user_by_id(user_id=user.id)
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail=ErrorEnum.USER_NOT_FOUND.value)

        user_data_manager.deactivate_user(user=user)
        return user


class UserDataManager(BaseDataManager):

    def get_user_by_id(self, user_id) -> [UserModel]:
        return self.get_one(model=UserModel, id=user_id)

    def get_user_by_email(self, email: str) -> UserModel:
        return self.get_one(UserModel, email=email)

    def get_user_by_login(self, login) -> UserModel:
        return self.get_one(UserModel, login=login)

    def get_all_users(self) -> [UserModel]:
        return self.get_all(model=UserModel)

    def get_active_users(self) -> [UserModel]:
        return self.get_all(model=UserModel, is_active=True)

    def deactivate_user(self, user: DeactivateSchema) -> None:
        user.is_active = False
        self.session.commit()

    def update_user(self, user: UserSchema, updated_data: dict):
        user = self.get_user_by_id(user_id=user.id)
        if not user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=ErrorEnum.LOGIN_ALREADY_EXIST.value)
        for key, value in updated_data.items():
            setattr(user, key, value)
        self.update(model=user, update_data=updated_data)
