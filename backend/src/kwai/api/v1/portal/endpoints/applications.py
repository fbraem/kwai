"""Module that implements applications endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.schemas.application import ApplicationDocument
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


@router.get("/applications")
async def get_applications(
    db=Depends(create_database),
) -> ApplicationDocument:
    """Get all applications of kwai."""
    command = GetApplicationsCommand()
    count, application_iterator = await GetApplications(
        ApplicationDbRepository(db)
    ).execute(command)

    document = ApplicationDocument(meta=Meta(count=count), data=[])
    async for application in application_iterator:
        document.merge(ApplicationDocument.create(application))

    return document


@router.get("/applications/{id}")
async def get_application(
    id: int,
    db=Depends(create_database),
) -> ApplicationDocument:
    """Get application."""
    command = GetApplicationCommand(id=id)

    try:
        application = await GetApplication(ApplicationDbRepository(db)).execute(command)
    except ApplicationNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    return ApplicationDocument.create(application)


@router.patch("/applications/{id}")
async def update_application(
    id: int,
    resource: ApplicationDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> ApplicationDocument:
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

    return ApplicationDocument.create(application)
