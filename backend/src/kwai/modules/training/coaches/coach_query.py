"""Module that defines an interface for a coach query."""
from abc import ABC, abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.modules.training.coaches.coach import CoachIdentifier


class CoachQuery(Query, ABC):
    """Interface for a coach query."""

    @abstractmethod
    def filter_by_id(self, id_: CoachIdentifier) -> "CoachQuery":
        """Add a filter for a given id.

        Args:
            id_: A coach id.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_ids(self, *id_: CoachIdentifier) -> "CoachQuery":
        """Add a filter on one or more coach identifiers.

        Args:
            id_: one or more ids of a coach.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_active(self) -> "CoachQuery":
        """Add a filter for the active coaches."""
        raise NotImplementedError
