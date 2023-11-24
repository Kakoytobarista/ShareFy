from fastapi import Depends, Request, Response, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from data_managers.user import UserDataManager
from database.session import get_db
from enums import TokenEnum
from schemas.v1.token import AccessTokenSchema
from services.user import UserService
from utils.token import get_current_user, TokenManager, TokenService

router = APIRouter(prefix="/token")


@router.post("/refresh", response_model=AccessTokenSchema, dependencies=[Depends(get_current_user)])
async def get_access_token_by_refresh(
        request: Request, response: Response, session: AsyncSession = Depends(get_db)):
    user_service = UserService(managers=[UserDataManager(session=session)])
    token_service = TokenService(manager=TokenManager())

    refresh_token = await token_service.manager.get_refresh_token_from_store(request=request)
    user_email = await token_service.manager.decode_refresh_token(refresh_token=refresh_token)
    user_data = await user_service.manager.get_user_by_email(email=user_email)
    access_token = await token_service.get_access_token(user_data=user_data)
    new_refresh_token = await token_service.get_refresh_token(user_data=user_data)

    response.set_cookie(
        key=TokenEnum.TOKEN_KEY.value, value=access_token.access_token, expires=access_token.expired_date, httponly=True)
    response.set_cookie(
        key=TokenEnum.REFRESH_TOKEN_KEY.value, value=new_refresh_token.refresh_token, httponly=True)

    return access_token
