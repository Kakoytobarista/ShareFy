from fastapi import HTTPException, Depends
from starlette import status

from app.enums import ErrorEnum
from app.schemas.v1.user import PersonTypeSchema
from app.utils.token import get_current_user


class PermissionChecker:

    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    async def __call__(self, user: PersonTypeSchema = Depends(get_current_user)) -> bool:
        user = await user
        if user.person_type not in self.required_permissions:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorEnum.PERMISSION_ERROR.value
            )
        return True
