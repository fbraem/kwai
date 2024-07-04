"""Module that defines an interface for a team repository."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Self

from kwai.core.domain.repository.query import Query
from kwai.modules.teams.domain.team import TeamEntity, TeamIdentifier


class TeamNotFoundException(Exception):
    """Raised when a team cannot be found."""


class TeamQuery(Query, ABC):
    """An interface for a team query."""

    @abstractmethod
    def filter_by_id(self, id_: TeamIdentifier) -> Self:
        """Find a team by its id."""
        raise NotImplementedError


class TeamRepository(ABC):
    """An interface for a team repository."""

    @abstractmethod
    def create_query(self) -> TeamQuery:
        """Create a team query."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, query: TeamQuery | None = None) -> TeamEntity:
        """Return the first returned element of the given query.

        Args:
            query: The query to use for getting the first team.

        Raises:
            TeamNotFoundException: If the team cannot be found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        query: TeamQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncGenerator[TeamEntity, None]:
        """Return all teams of the given query.

        Args:
            query: The query to use for getting the teams.
            limit: The maximum number of teams to return.
            offset: The offset to use for fetching teams.

        Yields:
            A team entity.

        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, team: TeamEntity) -> TeamEntity:
        """Save a new team."""

    @abstractmethod
    async def delete(self, team: TeamEntity) -> None:
        """Delete a team."""
