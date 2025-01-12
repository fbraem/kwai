"""Module for testing the use case get_stories."""

from types import AsyncGeneratorType

import pytest

from kwai.modules.portal.get_news_items import GetNewsItems, GetNewsItemsCommand
from kwai.modules.portal.news.news_item_repository import NewsItemRepository


pytestmark = pytest.mark.db


async def test_get_stories(news_item_repo: NewsItemRepository):
    """Test the use case: get stories."""
    command = GetNewsItemsCommand()
    count, news_item_iterator = await GetNewsItems(news_item_repo).execute(command)

    assert count >= 0, "Count must be 0 or greater"
    assert isinstance(news_item_iterator, AsyncGeneratorType), (
        "A list of news items should be yielded"
    )

    news_item_dict = {news_item.id: news_item async for news_item in news_item_iterator}
    assert count == len(news_item_dict), "Count should be the same"
