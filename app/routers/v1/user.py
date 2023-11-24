from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.session import get_db
from data_managers.user import UserDataManager
from enums import EndpointPath, PersonTypeEnum
from permission import PermissionChecker
from schemas.v1.user import DeactivateSchema, PersonTypeSchema, UserSchema
from services.user import UserService
from utils.token import get_current_user

router = APIRouter(prefix="/user")


class SendMailDeactivateAccountError(Exception):
    pass


@router.get(EndpointPath.GET_ALL_USERS.value, response_model=List[UserSchema],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.REGULAR,
                                                                          PersonTypeEnum.ADMIN,
                                                                          PersonTypeEnum.MODERATOR]))])
async def get_all_users(session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    users = await user_service.get_all_users()
    return users


@router.get(EndpointPath.GET_USER.value, response_model=UserSchema,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.REGULAR,
                                                                          PersonTypeEnum.ADMIN,
                                                                          PersonTypeEnum.MODERATOR]))])
async def get_user(user_id: int, session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    user = await user_service.get_user(user=UserSchema(id=user_id))
    return user


@router.get(EndpointPath.GET_ACTIVE_USERS.value, response_model=List[UserSchema],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.MODERATOR,
                                                                          PersonTypeEnum.ADMIN,
                                                                          PersonTypeEnum.REGULAR]))])
async def get_active_users(session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    users = await user_service.get_active_users()
    return users


@router.put(EndpointPath.DEACTIVATE_USER.value, response_model=DeactivateSchema,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(
                              required_permissions=[PersonTypeEnum.ADMIN,
                                                    PersonTypeEnum.REGULAR,
                                                    PersonTypeEnum.MODERATOR]))])
async def deactivate_user(user_id: int, session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    user = await user_service.deactivate_user(user_id=user_id)
    return user


@router.post(EndpointPath.CHANGE_PERSON_TYPE.value, response_model=PersonTypeSchema,
             status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user),
                           Depends(PermissionChecker(required_permissions=[PersonTypeEnum.ADMIN,
                                                                           PersonTypeEnum.REGULAR,
                                                                           PersonTypeEnum.MODERATOR]))])
async def change_person_type(user: PersonTypeSchema, session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    user = await user_service.change_person_type(user=user)
    return user
