"""Module for defining the member repository interface."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Self

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.date import Date
from kwai.modules.teams.domain.team_member import MemberEntity, MemberIdentifier


class MemberNotFoundException(Exception):
    """Raised when a member does not exist."""


class MemberQuery(Query, ABC):
    """An interface for a member query."""

    @abstractmethod
    def filter_by_id(self, id_: MemberIdentifier) -> Self:
        """Find a team member by its id."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_birthdate(
        self, start_date: Date, end_date: Date | None = None
    ) -> Self:
        """Find team members by their birthdate."""
        raise NotImplementedError


class MemberRepository(ABC):
    """An interface for a member repository."""

    @abstractmethod
    def create_query(self) -> MemberQuery:
        """Create a query for querying team members."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, query: MemberQuery | None = None) -> MemberEntity:
        """Return the first returned element of the given query.

        Args:
            query: The query to use for getting the first member.

        Raises:
            MemberNotFoundException: If the member is not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        query: MemberQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncGenerator[MemberEntity, None]:
        """Return all members of the given query.

        Args:
            query: The query to use for getting the members.
            limit: The maximum number of members to return.
            offset: The offset to use for fetching members.

        Yields:
            A team member entity.
        """
        raise NotImplementedError
