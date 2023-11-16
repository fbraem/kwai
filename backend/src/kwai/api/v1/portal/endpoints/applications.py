"""Module that implements applications endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status

from kwai.api.dependencies import get_current_user
from kwai.api.schemas.application import (
    ApplicationResource,
)
from kwai.core.dependencies import create_database
from kwai.core.json_api import Meta
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.applications.application_repository import (
    ApplicationNotFoundException,
)
from kwai.modules.portal.get_application import GetApplication, GetApplicationCommand
from kwai.modules.portal.get_applications import GetApplications, GetApplicationsCommand
from kwai.modules.portal.update_application import (
    UpdateApplication,
    UpdateApplicationCommand,
)
from tests.core.domain.test_entity import UserEntity

router = APIRouter()


ApplicationResourceDocument = ApplicationResource.get_document_model()


@router.get("/applications")
async def get_applications(
    db=Depends(create_database),
) -> ApplicationResourceDocument:
    """Get all applications of kwai."""
    command = GetApplicationsCommand()
    count, application_iterator = await GetApplications(
        ApplicationDbRepository(db)
    ).execute(command)

    result: ApplicationResourceDocument = ApplicationResource.serialize_list(
        [ApplicationResource(application) async for application in application_iterator]
    )
    result.meta = Meta(count=count)

    return result


@router.get("/applications/{id}")
async def get_application(
    id: int,
    db=Depends(create_database),
) -> ApplicationResourceDocument:
    """Get application."""
    command = GetApplicationCommand(id=id)

    try:
        application = await GetApplication(ApplicationDbRepository(db)).execute(command)
    except ApplicationNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    result: ApplicationResourceDocument = ApplicationResource.serialize(
        ApplicationResource(application)
    )

    return result


@router.patch("/applications/{id}")
async def update_application(
    id: int,
    resource: ApplicationResource.get_resource_data_model(),
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> ApplicationResourceDocument:
    """Get application."""
    command = UpdateApplicationCommand(
        id=id,
        title=resource.data.attributes.title,
        short_description=resource.data.attributes.short_description,
        description=resource.data.attributes.description,
        remark=resource.data.attributes.remark,
        weight=resource.data.attributes.weight,
        events=resource.data.attributes.events,
        pages=resource.data.attributes.pages,
        news=resource.data.attributes.news,
    )

    try:
        application = await UpdateApplication(ApplicationDbRepository(db)).execute(
            command
        )
    except ApplicationNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    return ApplicationResource.serialize(ApplicationResource(application))
