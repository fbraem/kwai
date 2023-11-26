"""Module that implements the endpoints for news."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from kwai.api.dependencies import get_current_user, get_optional_user
from kwai.api.schemas.news_item import NewsItemResource
from kwai.core.dependencies import create_database
from kwai.core.domain.use_case import TextCommand
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.create_news_item import CreateNewsItem, CreateNewsItemCommand
from kwai.modules.portal.delete_news_item import DeleteNewsItem, DeleteNewsItemCommand
from kwai.modules.portal.get_news_item import GetNewsItem, GetNewsItemCommand
from kwai.modules.portal.get_news_items import GetNewsItems, GetNewsItemsCommand
from kwai.modules.portal.news.news_item_db_repository import NewsItemDbRepository
from kwai.modules.portal.news.news_item_repository import NewsItemNotFoundException
from kwai.modules.portal.update_news_item import UpdateNewsItem, UpdateNewsItemCommand

router = APIRouter()


class NewsFilterModel(BaseModel):
    """Define the JSON:API filter for news."""

    enabled: bool = Field(Query(default=True, alias="filter[enabled]"))
    publish_year: int = Field(Query(default=0, alias="filter[publish_year]"))
    publish_month: int = Field(Query(default=0, alias="filter[publish_month]"))
    application: str | None = Field(Query(default=None, alias="filter[application]"))
    promoted: bool = Field(Query(default=False, alias="filter[promoted]"))
    author: str | None = Field(Query(default=None, alias="filter[author]"))


@router.get("/news_items")
async def get_news_items(
    pagination: PaginationModel = Depends(PaginationModel),
    news_filter: NewsFilterModel = Depends(NewsFilterModel),
    db=Depends(create_database),
    user: UserEntity | None = Depends(get_optional_user),
) -> NewsItemResource.get_document_model():
    """Get news items."""
    # Only a know user is allowed to see disabled news.
    if user is None and not news_filter.enabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    command = GetNewsItemsCommand(
        offset=pagination.offset or 0,
        limit=pagination.limit or 10,
        enabled=news_filter.enabled,
        publish_year=news_filter.publish_year,
        publish_month=news_filter.publish_month,
        application=news_filter.application,
        promoted=news_filter.promoted,
        author_uuid=news_filter.author,
    )
    count, news_item_iterator = await GetNewsItems(NewsItemDbRepository(db)).execute(
        command
    )

    document = NewsItemResource.serialize_list(
        [NewsItemResource(news_item) async for news_item in news_item_iterator]
    )
    document.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return document


@router.get("/news_items/{id}")
async def get_news_item(
    id: int,
    db=Depends(create_database),
    user: UserEntity | None = Depends(get_optional_user),
) -> NewsItemResource.get_document_model():
    """Get a news item."""
    command = GetNewsItemCommand(id=id)

    try:
        news_item = await GetNewsItem(NewsItemDbRepository(db)).execute(command)
    except NewsItemNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    # Only a know user is allowed to see disabled news.
    if not user and not news_item.is_enabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return NewsItemResource.serialize(NewsItemResource(news_item))


@router.post("/news_items", status_code=status.HTTP_201_CREATED)
async def create_news_item(
    resource: NewsItemResource.get_resource_data_model(),
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> NewsItemResource.get_document_model():
    """Create a new news item."""
    command = CreateNewsItemCommand(
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
        publish_datetime=resource.data.attributes.publish_date,
        end_datetime=resource.data.attributes.end_date,
        promotion=resource.data.attributes.priority,
        promotion_end_datetime=resource.data.attributes.promotion_end_date,
        remark=resource.data.attributes.remark,
    )
    news_item = await CreateNewsItem(
        NewsItemDbRepository(db),
        ApplicationDbRepository(db),
        Owner(id=user.id, uuid=user.uuid, name=user.name),
    ).execute(command)

    return NewsItemResource.serialize(NewsItemResource(news_item))


@router.patch(
    "/news_items/{id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "News item was not found."}},
)
async def update_news_item(
    id: int,
    resource: NewsItemResource.get_resource_data_model(),
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> NewsItemResource.get_document_model():
    """Update a new news item."""
    command = UpdateNewsItemCommand(
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
        publish_datetime=resource.data.attributes.publish_date,
        end_datetime=resource.data.attributes.end_date,
        promotion=resource.data.attributes.priority,
        promotion_end_datetime=resource.data.attributes.promotion_end_date,
        remark=resource.data.attributes.remark,
    )
    try:
        news_item = await UpdateNewsItem(
            NewsItemDbRepository(db),
            ApplicationDbRepository(db),
            Owner(id=user.id, uuid=user.uuid, name=user.name),
        ).execute(command)
    except NewsItemNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    return NewsItemResource.serialize(NewsItemResource(news_item))


@router.delete(
    "/news_items/{id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "News Item was not found."}},
)
async def delete_news_item(
    id: int,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
):
    """Delete a new news item."""
    command = DeleteNewsItemCommand(id=id)

    try:
        await DeleteNewsItem(NewsItemDbRepository(db)).execute(command)
    except NewsItemNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
