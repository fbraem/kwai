"""Module for defining a interface for a story query."""
from abc import abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.stories.story import StoryIdentifier


class StoryQuery(Query):
    """An interface for a story query."""

    @abstractmethod
    def filter_by_id(self, id_: StoryIdentifier) -> "StoryQuery":
        """Add a filter on the news story id.

        Args:
            id_: an id of a news story.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_publication_date(
        self, year: int, month: int | None = None
    ) -> "StoryQuery":
        """Add a filter on the publication date.

        Args:
            year: Only return news stories published in this year.
            month: Only return news stories published in this month.

        When month is omitted, all stories published in the given year will be returned.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_promoted(self) -> "StoryQuery":
        """Add a filter to return only the promoted news stories."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_application(self, application: int | str) -> "StoryQuery":
        """Add a filter to return only stories for the given application.

        Args:
            application: The id or the name of the application
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_active(self) -> "StoryQuery":
        """Add a filter to only return active news stories.

        An active story is enabled and is not expired.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_user(self, user: int | UniqueId) -> "StoryQuery":
        """Add a filter to only return news stories of the given user.

        Args:
            user: The id or unique id of the user.
        """
        raise NotImplementedError

    @abstractmethod
    def order_by_publication_date(self) -> "StoryQuery":
        """Order the result on the publication date."""
        raise NotImplementedError
