"""Module for defining an interface for a coach repository."""

from abc import ABC, abstractmethod

from kwai.modules.club.domain.coach import CoachEntity


class CoachRepository(ABC):
    """An interface for a coach repository."""

    @abstractmethod
    async def create(self, coach: CoachEntity):
        """Save a new coach."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, coach: CoachEntity):
        """Delete an existing coach."""
        raise NotImplementedError
