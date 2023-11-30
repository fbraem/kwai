"""Module for defining the pages endpoint."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from kwai.api.dependencies import get_current_user
from kwai.api.schemas.page import PageResource
from kwai.core.dependencies import create_database
from kwai.core.domain.use_case import TextCommand
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.applications.application_repository import (
    ApplicationNotFoundException,
)
from kwai.modules.portal.create_page import CreatePage, CreatePageCommand
from kwai.modules.portal.delete_page import DeletePage, DeletePageCommand
from kwai.modules.portal.get_page import GetPage, GetPageCommand
from kwai.modules.portal.get_pages import GetPages, GetPagesCommand
from kwai.modules.portal.pages.page_db_repository import PageDbRepository
from kwai.modules.portal.pages.page_repository import PageNotFoundException
from kwai.modules.portal.update_page import UpdatePage, UpdatePageCommand

router = APIRouter()


class PageFilter(BaseModel):
    """Define the JSON:API filter for pages."""

    application: str | None = Field(Query(default=None, alias="filter[application]"))


@router.get("/pages")
async def get_pages(
    pagination: PaginationModel = Depends(PaginationModel),
    page_filter: PageFilter = Depends(PageFilter),
    db=Depends(create_database),
) -> PageResource.get_document_model():
    """Get pages."""
    command = GetPagesCommand(
        offset=pagination.offset or 0,
        limit=pagination.limit,
        application=page_filter.application,
    )
    count, page_iterator = await GetPages(PageDbRepository(db)).execute(command)

    document = PageResource.serialize_list(
        [PageResource(page) async for page in page_iterator]
    )
    document.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return document


@router.get("/pages/{id}")
async def get_page(
    id: int,
    db=Depends(create_database),
) -> PageResource.get_document_model():
    """Get page."""
    command = GetPageCommand(id=id)
    page = await GetPage(PageDbRepository(db)).execute(command)

    document = PageResource.serialize(PageResource(page))

    return document


@router.post("/pages", status_code=status.HTTP_201_CREATED)
async def create_page(
    resource: PageResource.get_resource_data_model(),
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> PageResource.get_document_model():
    """Create a page."""
    command = CreatePageCommand(
        enabled=resource.data.attributes.enabled,
        texts=[
            TextCommand(
                locale=text.locale,
                format=text.format,
                title=text.title,
                summary=text.original_summary,
                content=text.original_content,
            )
            for text in resource.data.attributes.texts
        ],
        application=int(resource.data.relationships.application.data.id),
        priority=resource.data.attributes.priority,
        remark=resource.data.attributes.remark,
    )

    try:
        page = await CreatePage(
            PageDbRepository(db),
            ApplicationDbRepository(db),
            Owner(id=user.id, uuid=user.uuid, name=user.name),
        ).execute(command)
    except ApplicationNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex)
        ) from ex

    return PageResource.serialize(PageResource(page))


@router.patch("/pages/{id}")
async def update_page(
    id: int,
    resource: PageResource.get_resource_data_model(),
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> PageResource.get_document_model():
    """Update a page."""
    command = UpdatePageCommand(
        id=id,
        enabled=resource.data.attributes.enabled,
        texts=[
            TextCommand(
                locale=text.locale,
                format=text.format,
                title=text.title,
                summary=text.original_summary,
                content=text.original_content,
            )
            for text in resource.data.attributes.texts
        ],
        application=int(resource.data.relationships.application.data.id),
        priority=resource.data.attributes.priority,
        remark=resource.data.attributes.remark,
    )
    try:
        page = await UpdatePage(
            PageDbRepository(db),
            ApplicationDbRepository(db),
            Owner(id=user.id, uuid=user.uuid, name=user.name),
        ).execute(command)
    except ApplicationNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex)
        ) from ex

    return PageResource.serialize(PageResource(page))


@router.delete(
    "/pages/{id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Page was not found."}},
)
async def delete_news_item(
    id: int,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
):
    """Delete a page."""
    command = DeletePageCommand(id=id)

    try:
        await DeletePage(PageDbRepository(db)).execute(command)
    except PageNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
