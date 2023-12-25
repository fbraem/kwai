"""Module for defining the use case 'get coaches'."""
from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.modules.training.coaches.coach_repository import CoachRepository


class GetCoaches:
    """Use case for getting coaches."""

    def __init__(self, coach_repo: CoachRepository):
        """Initialize the use case.

        Args:
            coach_repo: The repository for getting the coaches.
        """
        self._coach_repo = coach_repo

    async def execute(self) -> UseCaseBrowseResult:
        """Execute the use case."""
        coach_query = self._coach_repo.create_query()
        count = await coach_query.count()

        return UseCaseBrowseResult(
            count=count,
            iterator=self._coach_repo.get_all(),
        )
