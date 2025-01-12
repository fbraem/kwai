"""Module that implements news endpoints."""

from fastapi import APIRouter, Depends

from kwai.api.dependencies import create_database
from kwai.api.schemas.news_item import NewsItemDocument
from kwai.core.db.database import Database
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.portal.get_news_items import GetNewsItems, GetNewsItemsCommand
from kwai.modules.portal.news.news_item_db_repository import NewsItemDbRepository


router = APIRouter()


@router.get("/news")
async def get_news(
    pagination: PaginationModel = Depends(PaginationModel),
    db: Database = Depends(create_database),
) -> NewsItemDocument:
    """Get news items for the portal.

    Only promoted news items are returned for the portal.
    """
    command = GetNewsItemsCommand(
        offset=pagination.offset or 0, limit=pagination.limit or 10, promoted=True
    )

    count, news_item_iterator = await GetNewsItems(NewsItemDbRepository(db)).execute(
        command
    )

    result = NewsItemDocument(
        meta=Meta(count=count, offset=command.offset, limit=command.limit), data=[]
    )

    async for news_item in news_item_iterator:
        news_document = NewsItemDocument.create(news_item)
        result.merge(news_document)

    return result
