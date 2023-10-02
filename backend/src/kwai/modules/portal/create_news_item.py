"""Module for defining the use case "Create News Item"."""
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.portal.applications.application import ApplicationIdentifier
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.news.news_item import NewsItemEntity, Promotion
from kwai.modules.portal.news.news_item_repository import NewsItemRepository
from kwai.modules.portal.news_item_command import NewsItemCommand

CreateNewsItemCommand = NewsItemCommand


class CreateNewsItem:
    """Use case "Create News Item"."""

    def __init__(
        self,
        repo: NewsItemRepository,
        application_repo: ApplicationRepository,
        owner: Owner,
    ):
        """Initialize the use case.

        Args:
            repo: The repository to create the news item.
            application_repo: The repository to get the application entity.
            owner: The owner of the news item.
        """
        self._repo = repo
        self._application_repo = application_repo
        self._owner = owner

    async def execute(self, command: CreateNewsItemCommand) -> NewsItemEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            ApplicationNotFoundException: raised when the application does not exist.
        """
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
        news_item = NewsItemEntity(
            enabled=command.enabled,
            promotion=promotion,
            period=Period(
                start_date=LocalTimestamp.create_from_string(command.publish_datetime),
                end_date=LocalTimestamp.create_from_string(command.end_datetime),
            ),
            application=application,
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
        )

        return await self._repo.create(news_item)
