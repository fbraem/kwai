"""Module that implements news endpoints."""

from fastapi import APIRouter, Depends

from kwai.api.dependencies import deps
from kwai.api.v1.portal.schemas.news_item import NewsItemResource
from kwai.core.db.database import Database
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.portal.get_news_items import GetNewsItems, GetNewsItemsCommand
from kwai.modules.portal.news.news_item_db_repository import NewsItemDbRepository

router = APIRouter()


@router.get("/news")
async def get_news(
    pagination: PaginationModel = Depends(PaginationModel), db=deps.depends(Database)
) -> NewsItemResource.get_document_model():
    """Get news items for the portal.

    Only promoted news items are returned for the portal.
    """
    command = GetNewsItemsCommand(
        offset=pagination.offset or 0, limit=pagination.limit or 10, promoted=True
    )
    count, news_item_iterator = await GetNewsItems(NewsItemDbRepository(db)).execute(
        command
    )

    document = NewsItemResource.serialize_list(
        [NewsItemResource(news_item) async for news_item in news_item_iterator]
    )
    document.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return document
