from sqlalchemy.orm import Session

from app.models.v1.user import UserModel
from app.schemas.v1.user import UserSchema
from app.services.base import BaseDataManager, BaseService


class UserService(BaseService):

    @staticmethod
    def get_user(user: UserSchema, session: Session) -> UserSchema:
        return UserDataManager(session=session).get_user_by_id(user_id=user.id)

    @staticmethod
    def get_all_users(session: Session) -> UserSchema:
        return UserDataManager(session=session).get_all_users()


class UserDataManager(BaseDataManager):

    def get_user_by_id(self, user_id) -> [UserSchema]:
        return self.get_one(model=UserModel, id=user_id)

    def get_user_by_email(self, email: str) -> UserModel:
        return self.get_one(UserModel, email=email)

    def get_user_by_login(self, login) -> UserModel:
        return self.get_one(UserModel, login=login)

    def get_all_users(self) -> [UserSchema]:
        return self.get_all(model=UserModel)
