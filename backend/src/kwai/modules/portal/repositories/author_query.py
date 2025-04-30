"""Module that defines an interface for an Author query."""

from abc import ABC, abstractmethod
from typing import Self

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorIdentifier


class AuthorQuery(Query, ABC):
    """An interface for an author query."""

    @abstractmethod
    def filter_by_id(self, id_: AuthorIdentifier) -> Self:
        """Filter an author on its id."""

    @abstractmethod
    def filter_by_uuid(self, uuid: UniqueId) -> Self:
        """Filter an author on its unique user id."""
