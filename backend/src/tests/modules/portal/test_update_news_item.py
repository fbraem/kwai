"""Module for testing the "Update News" use case."""
from kwai.core.domain.use_case import TextCommand
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.news.news_item import NewsItemEntity
from kwai.modules.portal.news.news_item_repository import NewsItemRepository
from kwai.modules.portal.update_news_item import UpdateNewsItem, UpdateNewsItemCommand


async def test_update_news(
    news_item_repo: NewsItemRepository,
    application_repo: ApplicationRepository,
    owner: Owner,
    saved_news_item: NewsItemEntity,
):
    """Test the "Update News" use case."""
    command = UpdateNewsItemCommand(
        id=saved_news_item.id.value,
        texts=[
            TextCommand(
                locale=text.locale.value,
                format=text.format.value,
                title=text.title,
                summary=text.summary,
                content=text.content,
            )
            for text in saved_news_item.texts
        ],
        application=saved_news_item.application.id.value,
        publish_datetime=str(saved_news_item.period.start_date),
        enabled=saved_news_item.is_enabled,
        end_datetime=str(saved_news_item.period.end_date),
        promotion=saved_news_item.promotion.priority,
        promotion_end_datetime=str(saved_news_item.promotion.end_date),
        remark="Updated with test_update_news_item",
    )
    updated_news_item = await UpdateNewsItem(
        news_item_repo, application_repo, owner
    ).execute(command)
    assert updated_news_item is not None, "There should be a an updated news item."
