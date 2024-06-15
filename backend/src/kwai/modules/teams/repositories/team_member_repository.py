"""Module for defining the team member repository interface."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Self

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.date import Date
from kwai.modules.teams.domain.team_member import MemberEntity, MemberIdentifier


class TeamMemberNotFoundException(Exception):
    """Raised when a team member does not exist."""


class TeamMemberQuery(Query, ABC):
    """An interface for a team member query."""

    @abstractmethod
    def find_by_id(self, id_: MemberIdentifier) -> Self:
        """Find a team member by its id."""
        raise NotImplementedError

    @abstractmethod
    def find_by_birthdate(self, start_date: Date, end_date: Date | None = None) -> Self:
        """Find team members by their birthdate."""
        raise NotImplementedError


class TeamMemberRepository(ABC):
    """An interface for a team member repository."""

    @abstractmethod
    def create_query(self) -> TeamMemberQuery:
        """Create a query for querying team members."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, query: TeamMemberQuery | None = None) -> MemberEntity:
        """Return the first returned element of the given query.

        Args:
            query: The query to use for getting the first member.

        Raises:
            TeamMemberNotFoundException: If the team member is not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        query: TeamMemberQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncGenerator[MemberEntity, None]:
        """Return all team members of the given query.

        Args:
            query: The query to use for getting the members.
            limit: The maximum number of members to return.
            offset: The offset to use for fetching members.

        Yields:
            A team member entity.
        """
        raise NotImplementedError
