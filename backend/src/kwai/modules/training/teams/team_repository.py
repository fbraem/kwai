"""Module that defines an interface for a team repository."""
from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.training.teams.team import TeamEntity, TeamIdentifier
from kwai.modules.training.teams.team_query import TeamQuery


class TeamNotFoundException(Exception):
    """Raised when a team cannot be found."""


class TeamRepository(ABC):
    """Interface for a team repository."""

    @abstractmethod
    def create_query(self) -> TeamQuery:
        """Create a query for querying teams."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> AsyncIterator[TeamEntity]:
        """Get all teams."""

    @abstractmethod
    async def get_by_id(self, id: TeamIdentifier) -> TeamEntity:
        """Get the team with the given id.

        Args:
            id: An id of a team.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, *ids: TeamIdentifier) -> AsyncIterator[TeamEntity]:
        """Get all teams for the given ids.

        Args:
            ids: A variable number of team ids.
        """
        raise NotImplementedError
