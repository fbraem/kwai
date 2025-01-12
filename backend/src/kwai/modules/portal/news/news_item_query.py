"""Module for defining an interface for a news item query."""

from abc import abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.news.news_item import NewsItemIdentifier


class NewsItemQuery(Query):
    """An interface for a news item query."""

    @abstractmethod
    def filter_by_id(self, id_: NewsItemIdentifier) -> "NewsItemQuery":
        """Add a filter on the news item id.

        Args:
            id_: an id of a news item.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_publication_date(
        self, year: int, month: int | None = None
    ) -> "NewsItemQuery":
        """Add a filter on the publication date.

        Args:
            year: Only return news items published in this year.
            month: Only return news items published in this month.

        When month is omitted, all news items published in the given year will be
        returned.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_promoted(self) -> "NewsItemQuery":
        """Add a filter to return only the promoted news items."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_application(self, application: int | str) -> "NewsItemQuery":
        """Add a filter to return only news items for the given application.

        Args:
            application: The id or the name of the application
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_active(self) -> "NewsItemQuery":
        """Add a filter to only return active news items.

        An active news item is enabled and is not expired.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_user(self, user: int | UniqueId) -> "NewsItemQuery":
        """Add a filter to only return news items of the given user.

        Args:
            user: The id or unique id of the user.
        """
        raise NotImplementedError

    @abstractmethod
    def order_by_publication_date(self) -> "NewsItemQuery":
        """Order the result on the publication date."""
        raise NotImplementedError
