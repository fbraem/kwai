"""Implement the use case: get news items."""
from dataclasses import dataclass

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.news.news_item_repository import NewsItemRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetNewsItemsCommand:
    """Input for use case: [GetNewsItems][kwai.modules.news.get_news_items.GetNewsItems].

    Attributes:
        offset: Offset to use. Default is None.
        limit: The max. number of elements to return. Default is None, which means all.
        enabled: When False, also news items that are not activated will be returned.
    """

    offset: int | None = None
    limit: int | None = None
    enabled: bool = True
    publish_year: int = 0
    publish_month: int = 0
    application: int | str | None = None
    promoted: bool = False
    author_uuid: str | None = None


class GetNewsItems:
    """Implementation of the use case.

    Use this use case for getting news items.
    """

    def __init__(self, repo: NewsItemRepository):
        """Initialize the use case.

        Args:
            repo: A repository for getting the news items.
        """
        self._repo = repo

    async def execute(self, command: GetNewsItemsCommand) -> UseCaseBrowseResult:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            A tuple with the number of entities and an iterator for news item entities.
        """
        query = self._repo.create_query()

        if command.enabled:
            query.filter_by_active()

        if command.publish_year > 0:
            query.filter_by_publication_date(
                command.publish_year, command.publish_month
            )

        if command.promoted:
            query.filter_by_promoted()

        if command.application is not None:
            query.filter_by_application(command.application)

        if command.author_uuid is not None:
            query.filter_by_user(UniqueId.create_from_string(command.author_uuid))

        query.order_by_publication_date()

        return UseCaseBrowseResult(
            count=await query.count(),
            iterator=self._repo.get_all(
                query=query, offset=command.offset, limit=command.limit
            ),
        )
