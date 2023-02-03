"""Module that implements all user endpoints."""
from fastapi import APIRouter, Depends

from kwai.api.dependencies import get_current_user
from kwai.core.security.system_user import SystemUser

router = APIRouter()


@router.get("/user")
async def get(user: SystemUser = Depends(get_current_user)):
    """Get the current user."""
    return {"id": str(user.uuid)}
