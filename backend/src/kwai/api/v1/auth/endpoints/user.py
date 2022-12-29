from fastapi import APIRouter, Depends

from kwai.core.security import get_current_user, SystemUser

router = APIRouter()


@router.get("/user")
async def get(user: SystemUser = Depends(get_current_user)):
    return {"id": str(user.uuid)}
