"""Module that defines an interface for a training query."""

from abc import ABC, abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.training.coaches.coach import CoachEntity
from kwai.modules.training.teams.team import TeamEntity
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity


class TrainingQuery(Query, ABC):
    """Interface for a training query."""

    @abstractmethod
    def filter_by_id(self, id_: TrainingIdentifier) -> "TrainingQuery":
        """Add a filter on a training identifier.

        Args:
            id_: id of a training.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_year_month(
        self, year: int, month: int | None = None
    ) -> "TrainingQuery":
        """Add filter to get only trainings for the given year/month.

        Args:
            year: The year to use for the filter.
            month: The month to use for the filter.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_dates(self, start: Timestamp, end: Timestamp) -> "TrainingQuery":
        """Add filter to get only trainings between two dates.

        Args:
            start: The start date to use for the filter.
            end: The end date to use for the filter.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_coach(self, coach: CoachEntity) -> "TrainingQuery":
        """Add filter to get only trainings for the given week.

        Args:
            coach: The coach to use for the filter.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_team(self, team: TeamEntity) -> "TrainingQuery":
        """Add filter to get only trainings for the given team.

        Args:
            team: The team to use for the filter.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_definition(
        self, definition: TrainingDefinitionEntity
    ) -> "TrainingQuery":
        """Add filter to get only trainings for the given definition.

        Args:
            definition: The definition to use for the filter.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_active(self) -> "TrainingQuery":
        """Add filter to get only the active trainings."""
        raise NotImplementedError

    @abstractmethod
    def order_by_date(self) -> "TrainingQuery":
        """Order the trainings by date."""
        raise NotImplementedError
