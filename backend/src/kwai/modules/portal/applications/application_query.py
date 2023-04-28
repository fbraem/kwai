"""Module that defines an interface for an application query."""
from abc import abstractmethod, ABC

from kwai.core.domain.repository.query import Query
from kwai.modules.portal.applications.application import ApplicationIdentifier


class ApplicationQuery(Query, ABC):
    """An interface for querying applications."""

    @abstractmethod
    def filter_by_id(self, id_: ApplicationIdentifier) -> "ApplicationQuery":
        """Add a filter on the application id.

        Args:
            id_: an id of an application.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_name(self, name: str) -> "ApplicationQuery":
        """Add a filter on the application name.

        Args:
            name: the name of an application.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_only_news(self) -> "ApplicationQuery":
        """Only return applications which can contain news."""
        raise NotImplementedError

    @abstractmethod
    def filter_only_pages(self) -> "ApplicationQuery":
        """Only return applications which can contain pages."""
        raise NotImplementedError

    @abstractmethod
    def filter_only_events(self) -> "ApplicationQuery":
        """Only return applications which can contain events."""
        raise NotImplementedError
