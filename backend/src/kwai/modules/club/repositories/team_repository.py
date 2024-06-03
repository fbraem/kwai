"""Module that defines an interface for a team repository."""

from abc import ABC, abstractmethod

from kwai.modules.club.domain.team import TeamEntity


class TeamRepository(ABC):
    """An interface for a team repository."""

    @abstractmethod
    async def create(self, team: TeamEntity) -> TeamEntity:
        """Save a new team."""

    @abstractmethod
    async def delete(self, team: TeamEntity) -> None:
        """Delete a team."""
