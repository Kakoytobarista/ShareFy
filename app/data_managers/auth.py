from data_managers.base import SQLAlchemyDataManager


class AuthDataManager(SQLAlchemyDataManager):
    async def create_user(self, user_model) -> None:
        await self.create(user_model)
