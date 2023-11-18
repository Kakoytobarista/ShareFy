from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from enums import ErrorEnum
from schemas.v1.user import DeactivateSchema, PersonTypeSchema, UserSchema
from services.base import BaseService


class UserService(BaseService):
    def __init__(self, managers):
        super().__init__(managers=managers)

    def get_user(self, user: UserSchema) -> UserSchema:
        return self.manager.get_user_by_id(user_id=user.id)

    async def get_all_users(self) -> List[UserSchema]:
        return await self.manager.get_all_users()

    async def get_active_users(self) -> UserSchema:
        return await self.manager.get_active_users()

    async def deactivate_user(self, user_id: int):
        user = await self.manager.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail=ErrorEnum.USER_NOT_FOUND.value)

        await self.manager.deactivate_user(user_model=user)
        saved_user = await self.manager.get_user_by_id(user_id=user_id)
        user_schema = DeactivateSchema(id=saved_user.id,
                                       is_active=saved_user.is_active)
        return user_schema

    async def change_person_type(self, user: PersonTypeSchema):
        user_model = await self.manager.get_user_by_id(user_id=user.id)
        if not user_model:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail=ErrorEnum.USER_NOT_FOUND.value)
        await self.manager.update_user(user_model=user_model, updated_data=user.model_dump())
        return user
