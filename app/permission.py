import enum

from fastapi import Depends, HTTPException
from starlette import status

from enums import ErrorEnum
from logger import logger
from schemas.v1.user import PersonTypeSchema
from utils.token import get_current_user


class PermissionChecker:

    def __init__(self, required_permissions: list[enum]) -> None:
        self.required_permissions = required_permissions

    async def __call__(self, user: PersonTypeSchema = Depends(get_current_user)) -> bool:
        user = user
        logger.debug(f"User: {user}, has person type {user.person_type}")
        if user.person_type not in self.required_permissions:
            logger.error(f"User: {user}, has person type: {user.person_type} not in allowed group: {self.required_permissions}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorEnum.PERMISSION_ERROR.value
            )
        return True
