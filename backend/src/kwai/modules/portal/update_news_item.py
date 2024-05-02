"""Module for implementing the use case "Update News Item"."""

from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.core.domain.value_objects.timestamp import LocalTimestamp
from kwai.modules.portal.applications.application import ApplicationIdentifier
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.news.news_item import (
    NewsItemEntity,
    NewsItemIdentifier,
    Promotion,
)
from kwai.modules.portal.news.news_item_repository import NewsItemRepository
from kwai.modules.portal.news_item_command import NewsItemCommand


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateNewsItemCommand(NewsItemCommand):
    """Input for the use case "Update News Item"."""

    id: int


class UpdateNewsItem:
    """Use case for updating a news item."""

    def __init__(
        self,
        repo: NewsItemRepository,
        application_repo: ApplicationRepository,
        owner: Owner,
    ):
        """Initialize the use case.

        Args:
            repo: A repository for updating news items.
            application_repo: A repository for getting the application.
            owner: The owner of the news item.
        """
        self._repo = repo
        self._application_repo = application_repo
        self._owner = owner

    async def execute(self, command: UpdateNewsItemCommand) -> NewsItemEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            NewsItemNotFoundException: When the news item does not exist.
            ApplicationNotFoundException: When the application does not exist.
        """
        news_item = await self._repo.get_by_id(NewsItemIdentifier(command.id))
        application = await self._application_repo.get_by_id(
            ApplicationIdentifier(command.application)
        )

        if command.promotion > 0:
            if command.promotion_end_datetime is None:
                promotion = Promotion(priority=command.promotion)
            else:
                promotion = Promotion(
                    priority=command.promotion,
                    end_date=LocalTimestamp.create_from_string(
                        command.promotion_end_datetime
                    ),
                )
        else:
            promotion = None

        news_item = Entity.replace(
            news_item,
            enabled=command.enabled,
            application=application,
            promotion=promotion,
            period=Period(
                start_date=LocalTimestamp.create_from_string(command.publish_datetime),
                end_date=(
                    None
                    if command.end_datetime
                    else LocalTimestamp.create_from_string(command.end_datetime)
                ),
            ),
            texts=[
                LocaleText(
                    locale=Locale(text.locale),
                    format=DocumentFormat(text.format),
                    title=text.title,
                    content=text.content,
                    summary=text.summary,
                    author=self._owner,
                )
                for text in command.texts
            ],
            remark=command.remark,
            traceable_time=news_item.traceable_time.mark_for_update(),
        )

        await self._repo.update(news_item)

        return news_item
