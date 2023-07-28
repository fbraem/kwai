"""Module that defines the trainings API."""

from fastapi import APIRouter

from kwai.api.dependencies import deps
from kwai.core.db.database import Database

router = APIRouter(prefix="/trainings", tags=["trainings"])


@router.get("/")
async def get_trainings(db=deps.depends(Database)):
    """Get all trainings."""
    pass
