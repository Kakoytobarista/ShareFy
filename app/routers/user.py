from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.session import get_db
from app.data_managers.user import UserDataManager
from app.enums import PersonTypeEnum
from app.permission import PermissionChecker
from app.schemas.v1.user import UserSchema, DeactivateSchema, PersonTypeSchema
from app.services.user import UserService
from app.utils.token import get_current_user

router = APIRouter(prefix="/user")


class SendMailDeactivateAccountError(Exception):
    pass

@router.get("/get_all_users", response_model=List[UserSchema],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.REGULAR.value,
                                                                          PersonTypeEnum.ADMIN.value, ]))])
async def get_all_users(session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    users = await user_service.get_all_users()
    return users


@router.get("/get_user/{user_id}", response_model=UserSchema,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.REGULAR.value,
                                                                          PersonTypeEnum.ADMIN.value, ]))])
async def get_user(user_id: int, session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    user = await user_service.get_user(user=UserSchema(id=user_id))
    return user


@router.get("/get_active_users", response_model=List[UserSchema],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.MODERATOR.value,
                                                                          PersonTypeEnum.ADMIN.value,
                                                                          PersonTypeEnum.REGULAR.value]))])
async def get_active_users(session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    users = await user_service.get_active_users()
    return users


@router.get("/deactivate_user/{user_id}", response_model=DeactivateSchema,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(
                              required_permissions=[PersonTypeEnum.ADMIN.value, PersonTypeEnum.REGULAR.value]))])
async def deactivate_user(user_id: int, session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    user = await user_service.deactivate_user(user_id=user_id)
    return user


@router.post("/change_person_type", response_model=PersonTypeSchema,
             status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user),
                           Depends(PermissionChecker(required_permissions=[PersonTypeEnum.ADMIN.value,
                                                                           PersonTypeEnum.REGULAR.value]))])
async def change_person_type(user: PersonTypeSchema, session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    user = await user_service.change_person_type(user=user)
    return user
