"""Module that implements all user endpoints."""

from fastapi import APIRouter, Depends

from kwai.api.dependencies import get_current_user
from kwai.modules.identity.users.user import UserEntity

router = APIRouter()


@router.get(
    "/user",
    summary="Get the id of the current user",
    responses={
        200: {"description": "Ok."},
        401: {"description": "Not authorized"},
    },
)
def get(user: UserEntity = Depends(get_current_user)):
    """Get the current user."""
    return {"id": str(user.uuid)}
