"""Module for the use case get trainings."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.modules.training.coaches.coach import CoachIdentifier
from kwai.modules.training.coaches.coach_repository import CoachRepository
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)
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

    def __init__(
        self,
        repo: TrainingRepository,
        coach_repo: CoachRepository,
        training_definition_repo: TrainingDefinitionRepository,
    ):
        """Initialize use case.

        Attributes:
            repo: The repository for trainings.
            coach_repo: The repository for coaches.
            training_definition_repo: The repository for training definitions.
        """
        self._repo = repo
        self._coach_repo = coach_repo
        self._training_definition_repo = training_definition_repo

    async def execute(self, command: GetTrainingsCommand) -> UseCaseBrowseResult:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            CoachNotFoundException: Raised when a coach is not found.
            TrainingDefinitionNotFoundException: Raised when a definition is not found.

        Returns:
            A tuple with the number of entities and an iterator for training entities.
        """
        query = self._repo.create_query().order_by_date()

        if command.year:
            query.filter_by_year_month(command.year, command.month)

        if command.start and command.end:
            query.filter_by_dates(command.start, command.end)

        if command.coach:
            coach = await self._coach_repo.get_by_id(CoachIdentifier(command.coach))
            query.filter_by_coach(coach)

        if command.definition:
            definition = await self._training_definition_repo.get_by_id(
                TrainingDefinitionIdentifier(command.definition)
            )
            query.filter_by_definition(definition)

        if command.active:
            query.filter_active()

        query.order_by_date()

        return UseCaseBrowseResult(
            count=await query.count(),
            iterator=self._repo.get_all(query, command.limit, command.offset),
        )
