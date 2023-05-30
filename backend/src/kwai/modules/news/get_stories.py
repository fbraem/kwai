"""Implement the use case: get news stories."""

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.news.stories.story_repository import StoryRepository

# pylint: disable=too-few-public-methods


class GetStoriesCommand:
    """Input for use case:
    [GetStories][kwai.modules.news.get_stories.GetStories]

    Attributes:
        offset: Offset to use. Default is None.
        limit: The max. number of elements to return. Default is None, which means all.
        enabled: When False, also stories that are not activated will be returned.
    """

    offset: int | None = None
    limit: int | None = None
    enabled: bool = True
    publish_year: int = 0
    publish_month: int = 0
    application: int | str | None = None
    promoted: bool = False
    author_uuid: str | None = None


class GetStories:
    """Implementation of the use case.

    Use this use case for getting news stories.
    """

    def __init__(self, repo: StoryRepository):
        """Initialize the use case.

        Args:
            repo: A repository for getting the news stories.
        """
        self._repo = repo

    async def execute(self, command: GetStoriesCommand) -> UseCaseBrowseResult:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            A tuple with the number of entities and an iterator for story entities.
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
