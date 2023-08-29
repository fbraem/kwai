"""Module that defines an interface for a team repository."""
from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.training.teams.team import TeamEntity, TeamIdentifier


class TeamRepository(ABC):
    """Interface for a team repository."""

    @abstractmethod
    async def get_by_ids(self, *ids: TeamIdentifier) -> AsyncIterator[TeamEntity]:
        """Get all teams for the given ids.

        Args:
            ids: A variable number of team ids.
        """
        raise NotImplementedError
