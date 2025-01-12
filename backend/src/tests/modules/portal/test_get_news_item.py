"""Module for testing the use case "Get News Item"."""

from kwai.modules.portal.get_news_item import GetNewsItem, GetNewsItemCommand
from kwai.modules.portal.news.news_item import NewsItemEntity
from kwai.modules.portal.news.news_item_repository import NewsItemRepository


async def test_get_news_item(
    news_item_repo: NewsItemRepository, saved_news_item: NewsItemEntity
):
    """Test get news item."""
    command = GetNewsItemCommand(id=saved_news_item.id.value)
    news_item = await GetNewsItem(news_item_repo).execute(command)
    assert news_item is not None, "There should be a news item."
