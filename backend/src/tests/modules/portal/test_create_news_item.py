"""Module for testing the use case "Create News Item"."""

import pytest

from kwai.core.domain.use_case import TextCommand
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_repository import (
    ApplicationNotFoundException,
    ApplicationRepository,
)
from kwai.modules.portal.create_news_item import CreateNewsItem, CreateNewsItemCommand
from kwai.modules.portal.news.news_item_repository import NewsItemRepository


async def test_create_news_item(
    news_item_repo: NewsItemRepository,
    application: ApplicationEntity,
    application_repo: ApplicationRepository,
    owner: Owner,
):
    """Test "Create News Item" use case."""
    command = CreateNewsItemCommand(
        enabled=True,
        texts=[
            TextCommand(
                locale="en",
                format="md",
                title="Test",
                summary="This is a test",
                content="This is a test",
            )
        ],
        application=application.id.value,
        publish_datetime="2023-01-01 00:00:00",
        end_datetime=None,
        promotion=0,
        promotion_end_datetime=None,
        remark="Created with test_create_news_item",
    )
    news_item = await CreateNewsItem(news_item_repo, application_repo, owner).execute(
        command
    )
    assert news_item is not None, "There should be a news item."


async def test_create_news_item_with_wrong_application(
    news_item_repo: NewsItemRepository,
    application: ApplicationEntity,
    application_repo: ApplicationRepository,
    owner: Owner,
):
    """Test "Create News Item" raising ApplicationNotFoundException."""
    command = CreateNewsItemCommand(
        enabled=True,
        texts=[
            TextCommand(
                locale="en",
                format="md",
                title="Test",
                summary="This is a test",
                content="This is a test",
            )
        ],
        application=0,
        publish_datetime="2023-01-01 00:00:00",
        end_datetime=None,
        promotion=0,
        promotion_end_datetime=None,
        remark="Created with test_create_news_item",
    )
    with pytest.raises(ApplicationNotFoundException):
        await CreateNewsItem(news_item_repo, application_repo, owner).execute(command)
