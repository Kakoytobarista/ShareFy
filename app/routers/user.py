from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.backend.session import SessionLocal, get_db
from app.backend.smtp import send_email_async
from app.enums import SubjectMailEnum, LetterNameEnum, PersonTypeEnum
from app.permission import PermissionChecker
from app.schemas.v1.user import UserSchema, DeactivateSchema, PersonTypeSchema
from app.services.user import UserDataManager, UserService
from app.utils.token import get_current_user

router = APIRouter(prefix="/user")
user_service = UserService(session=SessionLocal, manager=UserDataManager)


@router.get("/get_all_users", response_model=List[UserSchema],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.MODERATOR.value,
                                                                          PersonTypeEnum.ADMIN.value, ]))])
async def get_all_users(session: Session = Depends(get_db)):
    users = user_service.get_all_users(session=session)
    return users


@router.get("/get_user/{user_id}", response_model=UserSchema,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.MODERATOR.value,
                                                                          PersonTypeEnum.ADMIN.value, ]))])
async def get_all_users(user_id: int, session: Session = Depends(get_db)):
    print(user_id)
    user_schema = UserSchema(id=user_id)
    user = user_service.get_user(user=user_schema, session=session)
    return user


@router.get("/get_active_users", response_model=List[UserSchema],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user),
                          Depends(PermissionChecker(required_permissions=[PersonTypeEnum.MODERATOR.value,
                                                                          PersonTypeEnum.ADMIN.value, ]))])
async def get_active_users(session: Session = Depends(get_db)):
    users = user_service.get_active_users(session=session)
    return users


@router.post("/deactivate_user", response_model=UserSchema,
             status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user),
                           Depends(PermissionChecker(
                               required_permissions=[PersonTypeEnum.ADMIN.value, PersonTypeEnum.REGULAR.value]))])
async def deactivate_user(user: DeactivateSchema, session: Session = Depends(get_db)):
    user = user_service.deactivate_user(user=user, session=session)
    await send_email_async(subject=SubjectMailEnum.ACCOUNT_BLOCKED.value,  # TODO replace with push task in rabbitMQ and
                           # TODO handle it in celery
                           email_to=user.email,
                           template_path=LetterNameEnum.ACCOUNT_BLOCKED.value)
    return user


@router.post("/change_person_type", response_model=PersonTypeSchema,
             status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user),
                           Depends(PermissionChecker(required_permissions=[PersonTypeEnum.ADMIN.value, ]))])
async def change_person_type(user: PersonTypeSchema, session: Session = Depends(get_db)):
    user = user_service.change_person_type(user=user, session=session)
    return user
