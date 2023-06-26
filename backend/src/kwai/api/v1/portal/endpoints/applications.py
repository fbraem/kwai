"""Module that implements applications endpoints."""
from fastapi import APIRouter

from kwai.api.dependencies import deps
from kwai.api.schemas.application import (
    ApplicationResource,
)
from kwai.core.db.database import Database
from kwai.core.json_api import Meta
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.get_applications import GetApplicationsCommand, GetApplications

router = APIRouter()


@router.get("/applications")
async def get_applications(
    db=deps.depends(Database),
) -> ApplicationResource.get_document_model():
    """Get all applications of kwai."""
    command = GetApplicationsCommand()
    count, application_iterator = await GetApplications(
        ApplicationDbRepository(db)
    ).execute(command)

    document = ApplicationResource.serialize_list(
        [ApplicationResource(application) async for application in application_iterator]
    )
    document.meta = Meta(count=count)
