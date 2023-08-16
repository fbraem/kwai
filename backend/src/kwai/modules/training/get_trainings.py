"""Module for the use case get trainings."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.modules.training.coaches.coach import CoachEntity
from kwai.modules.training.trainings.training_repository import TrainingRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetTrainingsCommand:
    """Input for the get trainings use case.

    Attributes:
        limit: the max. number of elements to return. Default is None, which means all.
        offset: Offset to use. Default is None.
        year: Only return trainings of this year.
        month: Only return trainings of this month.
        start: Only return trainings starting from this date.
        end: Only return trainings before this date.
        coach: Only return trainings with this coach.
        definition: Only return trainings created from this definition.
        active: Only return trainings that are active (default is True).
    """

    limit: int | None = None
    offset: int | None = None
    year: int | None = None
    month: int | None = None
    start: datetime | None = None
    end: datetime | None = None
    coach: int | None = None
    definition: int | None = None
    active: bool = True


class GetTrainings:
    """Use case to get trainings."""

    def __init__(self, repo: TrainingRepository):
        self._repo = repo

    async def execute(self, command: GetTrainingsCommand) -> UseCaseBrowseResult:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            A tuple with the number of entities and an iterator for training entities.
        """
        query = self._repo.create_query().order_by_date()

        if command.year:
            query.filter_by_year_month(command.year, command.month)

        if command.start and command.end:
            query.filter_by_dates(command.start, command.end)

        if command.coach:
            query.filter_by_coach(CoachEntity(id=IntIdentifier(command.coach)))

        return UseCaseBrowseResult(
            count=await query.count(),
            iterator=self._repo.get_all(query, command.limit, command.offset),
        )
