from fastapi import APIRouter, Depends

from kwai.api.dependencies import get_current_user
from kwai.core.security import SystemUser

router = APIRouter()


@router.get("/user")
async def get(user: SystemUser = Depends(get_current_user)):
    return {"id": str(user.uuid)}
