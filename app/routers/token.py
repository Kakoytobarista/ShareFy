from fastapi import Depends, Request, Response, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from data_managers.user import UserDataManager
from database.session import get_db
from enums import TokenEnum, TokenTypeEnum
from schemas.v1.token import TokenResponseSchema
from services.user import UserService
from utils.token import get_current_user, decode_refresh_token, generate_access_token, get_refresh_token, \
    generate_refresh_token

router = APIRouter(prefix="/token")

@router.post("/refresh", response_model=TokenResponseSchema, dependencies=[Depends(get_current_user)])
async def get_access_token_by_refresh(request: Request, response: Response, session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    refresh_token = await get_refresh_token(request=request)
    user_email = decode_refresh_token(refresh_token=refresh_token)
    user_data = await user_service.manager.get_user_by_email(email=user_email)
    access_token_key, access_token, expired_date = await generate_access_token(user_data=user_data)
    new_refresh_token = await generate_refresh_token(user_data=user_data)
    response.set_cookie(key=access_token_key, value=access_token, expires=expired_date, httponly=True)
    response.set_cookie(key=TokenEnum.REFRESH_TOKEN_KEY.value, value=new_refresh_token, httponly=True)

    return TokenResponseSchema(
        access_token=access_token, refresh_token=new_refresh_token, token_type=TokenTypeEnum.BEARER.value, expired_date=expired_date)
