"""Module that defines the interface for a user account query."""

from abc import abstractmethod
from typing import Self

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user_account import UserAccountIdentifier


class UserAccountQuery(Query):
    """Interface for a user account query."""

    @abstractmethod
    def filter_by_id(self, id_: UserAccountIdentifier) -> Self:
        """Add a filter to the query with the id of the user."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_uuid(self, uuid: UniqueId) -> Self:
        """Add a filter to the query with the uuid of the user."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_email(self, email: EmailAddress) -> Self:
        """Add a filter to the query with the email of the user."""
        raise NotImplementedError
