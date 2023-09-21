"""Module for defining an interface for a page query."""
from abc import abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.pages.page import PageIdentifier


class PageQuery(Query):
    """An interface for a story query."""

    @abstractmethod
    def filter_by_id(self, id_: PageIdentifier) -> "PageQuery":
        """Add a filter on the news page id.

        Args:
            id_: an id of a page.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_application(self, application: int | str) -> "PageQuery":
        """Add a filter to return only pages for the given application.

        Args:
            application: The id or the name of the application
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_active(self) -> "PageQuery":
        """Add a filter to only return active pages."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_user(self, user: int | UniqueId) -> "PageQuery":
        """Add a filter to only return pages of the given user.

        Args:
            user: The id or unique id of the user.
        """
        raise NotImplementedError
