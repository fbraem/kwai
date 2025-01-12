"""Module that defines the use case "Get Training Definition"."""

from dataclasses import dataclass

from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class GetTrainingDefinitionCommand:
    """Input for the use case GetTrainingDefinition."""

    id: int


class GetTrainingDefinition:
    """Use case for getting a training definition."""

    def __init__(self, repo: TrainingDefinitionRepository):
        """Initialize the use case.

        Args:
            repo: A repository for getting the training definition.
        """
        self._repo = repo

    async def execute(
        self, command: GetTrainingDefinitionCommand
    ) -> TrainingDefinitionEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            TrainingDefinitionNotFoundException: raised when the training definition
                does not exist.
        """
        return await self._repo.get_by_id(TrainingDefinitionIdentifier(command.id))
