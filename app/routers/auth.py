from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.backend.session import SessionLocal, get_db
from app.schemas.v1.auth import CreateUserSchema, LoginSchema
from app.schemas.v1.token import TokenResponseSchema
from app.services.auth import AuthService, UserDataManager

router = APIRouter(prefix="/auth")
auth_service = AuthService(session=SessionLocal, manager=UserDataManager)


@router.post("/register", response_model=CreateUserSchema, status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserSchema, db_session: Session = Depends(get_db)):
    created_user = auth_service.create_user(user, db_session)
    return created_user


@router.post("/login", response_model=TokenResponseSchema, status_code=status.HTTP_200_OK)
async def login(login_data: LoginSchema, db_session: Session = Depends(get_db)):
    access_token = auth_service.login(login_data, db_session)
    return access_token
