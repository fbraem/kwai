"""Module that defines an interface for a team query."""

from abc import ABC, abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.modules.training.teams.team import TeamIdentifier


class TeamQuery(Query, ABC):
    """Interface for a team query."""

    @abstractmethod
    def filter_by_id(self, id_: TeamIdentifier) -> "TeamQuery":
        """Add a filter for a given id.

        Args:
            id_: A team id.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_ids(self, *id_: TeamIdentifier) -> "TeamQuery":
        """Add a filter on one or more team identifiers.

        Args:
            id_: one or more ids of a team.
        """
        raise NotImplementedError
