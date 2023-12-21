"""Module for defining the pages endpoint."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from kwai.api.converter import MarkdownConverter
from kwai.api.dependencies import get_current_user
from kwai.api.schemas.page import (
    PageApplicationAttributes,
    PageApplicationResource,
    PageAttributes,
    PageDocument,
    PageRelationships,
    PageResource,
    PageText,
)
from kwai.api.schemas.resources import ApplicationResourceIdentifier
from kwai.core.dependencies import create_database
from kwai.core.domain.use_case import TextCommand
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.json_api import Meta, PaginationModel, Relationship, ResourceMeta
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
from kwai.modules.portal.pages.page import PageEntity
from kwai.modules.portal.pages.page_db_repository import PageDbRepository
from kwai.modules.portal.pages.page_repository import PageNotFoundException
from kwai.modules.portal.update_page import UpdatePage, UpdatePageCommand

router = APIRouter()


def _create_resource(page: PageEntity) -> tuple[PageResource, PageApplicationResource]:
    return PageResource(
        id=str(page.id),
        meta=ResourceMeta(
            created_at=str(page.traceable_time.created_at),
            updated_at=str(page.traceable_time.updated_at),
        ),
        attributes=PageAttributes(
            enabled=page.enabled,
            priority=page.priority,
            remark=page.remark or "",
            texts=[
                PageText(
                    locale=text.locale.value,
                    format=text.format.value,
                    title=text.title,
                    summary=MarkdownConverter().convert(text.summary),
                    content=MarkdownConverter().convert(text.content)
                    if text.content
                    else None,
                    original_summary=text.summary,
                    original_content=text.content,
                )
                for text in page.texts
            ],
        ),
        relationships=PageRelationships(
            application=Relationship[ApplicationResourceIdentifier](
                data=ApplicationResourceIdentifier(id=str(page.application.id))
            )
        ),
    ), PageApplicationResource(
        id=str(page.application.id),
        attributes=PageApplicationAttributes(
            name=page.application.name, title=page.application.title
        ),
    )


class PageFilter(BaseModel):
    """Define the JSON:API filter for pages."""

    application: str | None = Field(Query(default=None, alias="filter[application]"))


@router.get("/pages")
async def get_pages(
    pagination: PaginationModel = Depends(PaginationModel),
    page_filter: PageFilter = Depends(PageFilter),
    db=Depends(create_database),
) -> PageDocument:
    """Get pages."""
    command = GetPagesCommand(
        offset=pagination.offset or 0,
        limit=pagination.limit,
        application=page_filter.application,
    )
    count, page_iterator = await GetPages(PageDbRepository(db)).execute(command)

    data: list[PageResource] = []
    included: set[PageApplicationResource] = set()

    async for page in page_iterator:
        page_resource, application_resource = _create_resource(page)
        data.append(page_resource)
        included.add(application_resource)

    return PageDocument(
        meta=Meta(count=count, offset=command.offset, limit=command.limit),
        data=data,
        included=included,
    )


@router.get("/pages/{id}")
async def get_page(
    id: int,
    db=Depends(create_database),
) -> PageDocument:
    """Get page."""
    command = GetPageCommand(id=id)
    page = await GetPage(PageDbRepository(db)).execute(command)

    page_resource, application_resource = _create_resource(page)
    return PageDocument(data=page_resource, included={application_resource})


@router.post("/pages", status_code=status.HTTP_201_CREATED)
async def create_page(
    resource: PageDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> PageDocument:
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

    page_resource, application_resource = _create_resource(page)
    return PageDocument(data=page_resource, included={application_resource})


@router.patch("/pages/{id}")
async def update_page(
    id: int,
    resource: PageDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> PageDocument:
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

    page_resource, application_resource = _create_resource(page)
    return PageDocument(data=page_resource, included={application_resource})


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
