"""Module for testing the use case "Delete News Item"."""
import pytest

from kwai.modules.portal.delete_news_item import DeleteNewsItem, DeleteNewsItemCommand
from kwai.modules.portal.get_news_item import GetNewsItem, GetNewsItemCommand
from kwai.modules.portal.news.news_item import NewsItemEntity
from kwai.modules.portal.news.news_item_repository import (
    NewsItemNotFoundException,
    NewsItemRepository,
)


async def test_delete_news_item(
    news_item_repo: NewsItemRepository, saved_news_item: NewsItemEntity
):
    """Test delete news item."""
    command = DeleteNewsItemCommand(id=saved_news_item.id.value)
    await DeleteNewsItem(news_item_repo).execute(command)

    command = GetNewsItemCommand(id=saved_news_item.id.value)
    with pytest.raises(NewsItemNotFoundException):
        await GetNewsItem(news_item_repo).execute(command)
