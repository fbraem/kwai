"""Module that defines the use case "Get Training Definitions"."""

from dataclasses import dataclass

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class GetTrainingDefinitionsCommand:
    """Input for the use case "Get Training Definitions"."""

    limit: int | None = None
    offset: int | None = None


class GetTrainingDefinitions:
    """Use case "Get Training Definitions"."""

    def __init__(self, repo: TrainingDefinitionRepository):
        """Initialize the use case.

        Args:
            repo: A repository for retrieving training definitions.
        """
        self._repo = repo

    async def execute(
        self, command: GetTrainingDefinitionsCommand
    ) -> UseCaseBrowseResult:
        """Execute the use case."""
        query = self._repo.create_query()

        return UseCaseBrowseResult(
            count=await query.count(),
            iterator=self._repo.get_all(query, command.limit, command.offset),
        )
