"""Module that defines an interface for a coach repository."""
from abc import ABC, abstractmethod

from kwai.modules.training.coaches.coach import CoachEntity, CoachIdentifier


class CoachNotFoundException(Exception):
    """Raised when a coach is not found."""


class CoachRepository(ABC):
    """Interface for a coach repository."""

    @abstractmethod
    async def get_by_id(self, id: CoachIdentifier) -> CoachEntity:
        """Get the coach with the given id.

        Args:
            id: The id of a coach.

        Raises:
            CoachNotFoundException: raised when the coach with the given id does not
                exist.
        """
        raise NotImplementedError
