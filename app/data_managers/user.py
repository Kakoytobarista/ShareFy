from typing import List

from app.data_managers.base import SQLAlchemyDataManager
from app.models.v1.user import UserModel


class UserDataManager(SQLAlchemyDataManager):

    async def get_user_by_id(self, user_id) -> UserModel:
        return await self.get(model=UserModel, id=user_id)

    async def get_user_by_email(self, email: str) -> UserModel:
        return await self.get(model=UserModel, email=email)

    async def get_user_by_login(self, login: str) -> UserModel:
        return await self.get(UserModel, login=login)

    async def get_all_users(self) -> List[UserModel]:
        return await self.get_all(model=UserModel)

    async def get_active_users(self) -> [UserModel]:
        return await self.get_all(model=UserModel, is_active=True)

    async def deactivate_user(self, user_model: UserModel) -> None:
        await self.update(model=user_model, updated_data={"is_active": False})
        await self.session.commit()

    async def update_user(self, user_model: UserModel, updated_data: dict) -> None:
        await self.update(model=user_model, updated_data=updated_data)
