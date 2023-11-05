from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.backend.session import SessionLocal, get_db
from app.schemas.v1.auth import CreateUserSchema, LoginSchema
from app.services.auth import AuthService, AuthDataManager
from app.utils.auth import create_access_token

router = APIRouter(prefix="/auth")
auth_service = AuthService(session=SessionLocal, manager=AuthDataManager)


@router.post("/register", response_model=CreateUserSchema, status_code=201)
async def register(user: CreateUserSchema, db: Session = Depends(get_db)):
    created_user = auth_service.create_user(user, db)
    return created_user


@router.post("/login", response_model=dict)
async def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    user = auth_service.login(login_data, db)
    access_token = create_access_token(data={"sub": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}
