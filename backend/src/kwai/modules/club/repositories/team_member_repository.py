"""Module for defining the team member repository interface."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from kwai.core.domain.repository.query import Query
from kwai.modules.club.domain.team_member import TeamMemberEntity


class TeamMemberNotFoundException(Exception):
    """Raised when a team member does not exist."""


class TeamMemberQuery(Query, ABC):
    """An interface for a team member query."""


class TeamMemberRepository(ABC):
    """An interface for a team member repository."""

    @abstractmethod
    def create_query(self) -> TeamMemberQuery:
        """Create a query for querying team members."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, query: TeamMemberQuery | None = None) -> TeamMemberEntity:
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
    ) -> AsyncGenerator[TeamMemberEntity, None]:
        """Return all team members of the given query.

        Args:
            query: The query to use for getting the members.
            limit: The maximum number of members to return.
            offset: The offset to use for fetching members.

        Yields:
            A team member entity.
        """
        raise NotImplementedError
