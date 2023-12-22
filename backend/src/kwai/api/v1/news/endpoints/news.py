"""Module that implements the endpoints for news."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from kwai.api.converter import MarkdownConverter
from kwai.api.dependencies import get_current_user, get_optional_user
from kwai.api.schemas.application import ApplicationBaseAttributes
from kwai.api.schemas.news_item import (
    NewsItemApplicationResource,
    NewsItemAttributes,
    NewsItemDocument,
    NewsItemRelationships,
    NewsItemResource,
    NewsItemText,
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
from kwai.modules.portal.create_news_item import CreateNewsItem, CreateNewsItemCommand
from kwai.modules.portal.delete_news_item import DeleteNewsItem, DeleteNewsItemCommand
from kwai.modules.portal.get_news_item import GetNewsItem, GetNewsItemCommand
from kwai.modules.portal.get_news_items import GetNewsItems, GetNewsItemsCommand
from kwai.modules.portal.news.news_item import NewsItemEntity
from kwai.modules.portal.news.news_item_db_repository import NewsItemDbRepository
from kwai.modules.portal.news.news_item_repository import NewsItemNotFoundException
from kwai.modules.portal.update_news_item import UpdateNewsItem, UpdateNewsItemCommand

router = APIRouter()


def _create_resource(
    news_item: NewsItemEntity,
) -> tuple[NewsItemResource, NewsItemApplicationResource]:
    return NewsItemResource(
        id=str(news_item.id),
        meta=ResourceMeta(
            created_at=str(news_item.traceable_time.created_at),
            updated_at=str(news_item.traceable_time.updated_at),
        ),
        attributes=NewsItemAttributes(
            priority=news_item.promotion.priority,
            publish_date=str(news_item.period.start_date),
            end_date=str(news_item.period.end_date),
            enabled=news_item.is_enabled,
            remark=news_item.remark or "",
            promotion_end_date=str(news_item.promotion.end_date),
            texts=[
                NewsItemText(
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
                for text in news_item.texts
            ],
        ),
        relationships=NewsItemRelationships(
            application=Relationship[ApplicationResourceIdentifier](
                data=ApplicationResourceIdentifier(id=str(news_item.application.id))
            )
        ),
    ), NewsItemApplicationResource(
        id=str(news_item.application.id),
        attributes=ApplicationBaseAttributes(
            name=news_item.application.name, title=news_item.application.title
        ),
    )


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
) -> NewsItemDocument:
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

    data: list[NewsItemResource] = []
    included: set[NewsItemApplicationResource] = set()

    async for news_item in news_item_iterator:
        news_item_resource, application_resource = _create_resource(news_item)
        data.append(news_item_resource)
        included.add(application_resource)

    return NewsItemDocument(
        meta=Meta(count=count, offset=command.offset, limit=command.limit),
        data=data,
        included=included,
    )


@router.get("/news_items/{id}")
async def get_news_item(
    id: int,
    db=Depends(create_database),
    user: UserEntity | None = Depends(get_optional_user),
) -> NewsItemDocument:
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

    news_item_resource, application_resource = _create_resource(news_item)
    return NewsItemDocument(
        data=news_item_resource,
        included={application_resource},
    )


@router.post("/news_items", status_code=status.HTTP_201_CREATED)
async def create_news_item(
    resource: NewsItemDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> NewsItemDocument:
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

    news_item_resource, application_resource = _create_resource(news_item)
    return NewsItemDocument(
        data=news_item_resource,
        included={application_resource},
    )


@router.patch(
    "/news_items/{id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "News item was not found."}},
)
async def update_news_item(
    id: int,
    resource: NewsItemDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> NewsItemDocument:
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

    news_item_resource, application_resource = _create_resource(news_item)
    return NewsItemDocument(
        data=news_item_resource,
        included={application_resource},
    )


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
