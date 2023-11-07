from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.backend.session import SessionLocal, get_db
from app.backend.smtp import send_email_async
from app.enums import SubjectMailEnum, LetterNameEnum
from app.schemas.v1.user import UserSchema, DeactivateSchema
from app.services.user import UserDataManager, UserService
from app.utils.token import get_current_user

router = APIRouter(prefix="/user")
user_service = UserService(session=SessionLocal, manager=UserDataManager)


@router.get("/get_all_users", response_model=List[UserSchema],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user), ])
async def get_all_users(session: Session = Depends(get_db)):
    users = user_service.get_all_users(session=session)
    return users


@router.get("/get_active_users", response_model=List[UserSchema],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user), ])
async def get_active_users(session: Session = Depends(get_db)):
    users = user_service.get_active_users(session=session)
    return users


@router.post("/deactivate_user", response_model=UserSchema,
             status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user)])
async def deactivate_user(user: DeactivateSchema, session: Session = Depends(get_db)):
    user = user_service.deactivate_user(user=user, session=session)
    await send_email_async(subject=SubjectMailEnum.ACCOUNT_BLOCKED.value,  # TODO replace with push task in rabbitMQ and
                                                                           # TODO handle it in celery
                           email_to=user.email,
                           template_path=LetterNameEnum.ACCOUNT_BLOCKED.value)
    return user
