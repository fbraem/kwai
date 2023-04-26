"""Module that implements applications endpoints."""
from fastapi import APIRouter

from kwai.api.dependencies import deps
from kwai.api.schemas.application import ApplicationsDocument, ApplicationData
from kwai.api.schemas.jsonapi import Meta
from kwai.core.db.database import Database

router = APIRouter()


@router.get("/applications")
def get_applications(db=deps.depends(Database)) -> ApplicationsDocument:
    """Get all applications of kwai."""
    result: list[ApplicationData] = []

    return ApplicationsDocument(meta=Meta(count=0), data=result)
