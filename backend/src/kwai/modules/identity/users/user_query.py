"""Module that defines the interface for a user query."""
from abc import abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserIdentifier


class UserQuery(Query):
    """Interface for a user query."""

    @abstractmethod
    def filter_by_id(self, id_: UserIdentifier) -> "UserQuery":
        """Add a filter to the query for the id of the user."""
        raise NotImplementedError

    def filter_by_uuid(self, uuid: UniqueId) -> "UserQuery":
        """Add a filter for a user with the given unique id."""
        raise NotImplementedError

    def filter_by_email(self, email: EmailAddress) -> "UserQuery":
        """Add a filter for a user with the given email address."""
        raise NotImplementedError
