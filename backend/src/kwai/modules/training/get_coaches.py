"""Module for defining the use case 'get coaches'."""
from dataclasses import dataclass

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.modules.training.coaches.coach_repository import CoachRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetCoachesCommand:
    """Input for the use case GetCoaches."""

    active: bool


class GetCoaches:
    """Use case for getting coaches."""

    def __init__(self, coach_repo: CoachRepository):
        """Initialize the use case.

        Args:
            coach_repo: The repository for getting the coaches.
        """
        self._coach_repo = coach_repo

    async def execute(self, command: GetCoachesCommand) -> UseCaseBrowseResult:
        """Execute the use case."""
        coach_query = self._coach_repo.create_query()

        if command.active:
            coach_query.filter_by_active()

        count = await coach_query.count()

        return UseCaseBrowseResult(
            count=count,
            iterator=self._coach_repo.get_all(coach_query),
        )
