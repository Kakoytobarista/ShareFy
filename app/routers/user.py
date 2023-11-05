from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.backend.session import SessionLocal, get_db
from app.schemas.v1.user import UserSchema
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
