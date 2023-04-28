"""Module that implements applications endpoints."""
from fastapi import APIRouter

from kwai.api.dependencies import deps
from kwai.api.schemas.application import (
    ApplicationsDocument,
    ApplicationData,
    ApplicationAttributes,
)
from kwai.api.schemas.jsonapi import Meta
from kwai.core.db.database import Database
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.get_applications import GetApplicationsCommand, GetApplications

router = APIRouter()


def _create_application_data(application: ApplicationEntity) -> ApplicationData:
    """Transform an application entity into a JSONAPI resource.

    Args:
        application: An application entity.

    Returns:
        A JSONAPI structure for an application resource.
    """
    return ApplicationData(
        id=str(application.id),
        attributes=ApplicationAttributes(
            name=application.name,
            title=application.title,
            description=application.description,
            short_description=application.short_description,
            remark=application.remark,
            news=application.can_contain_news,
            pages=application.can_contain_pages,
            events=application.can_contain_events,
            weight=application.weight,
            created_at=str(application.traceable_time.created_at),
            updated_at=(
                None
                if application.traceable_time.updated_at.empty
                else str(application.traceable_time.updated_at)
            ),
        ),
    )


@router.get("/applications")
async def get_applications(db=deps.depends(Database)) -> ApplicationsDocument:
    """Get all applications of kwai."""
    command = GetApplicationsCommand()
    count, applications = await GetApplications(ApplicationDbRepository(db)).execute(
        command
    )

    result: list[ApplicationData] = []
    async for application in applications:
        result.append(_create_application_data(application))

    return ApplicationsDocument(meta=Meta(count=count), data=result)
