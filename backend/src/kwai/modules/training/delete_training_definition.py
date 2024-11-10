"""Module for the use case "Delete Training Definition"."""

from dataclasses import dataclass

from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)
from kwai.modules.training.trainings.training_repository import TrainingRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class DeleteTrainingDefinitionCommand:
    """Input for the use case DeleteTrainingDefinition."""

    id: int
    delete_trainings: bool = False


class DeleteTrainingDefinition:
    """Use case "Delete Training Definition".

    When delete_trainings is True, Trainings that are related to this definition,
    will be. When False, the training will be updated.
    """

    def __init__(
        self, repo: TrainingDefinitionRepository, training_repo: TrainingRepository
    ):
        """Initialize the use case.

        Args:
            repo: A repository for deleting a training definition.
            training_repo: A repository for deleting or updating a training(s).
        """
        self._repo = repo
        self._training_repo = training_repo

    async def execute(self, command: DeleteTrainingDefinitionCommand):
        """Execute the use case.

        Raises:
            TrainingDefinitionNotFoundException: when the training definition
                does not exist.
        """
        training_definition = await self._repo.get_by_id(
            TrainingDefinitionIdentifier(command.id)
        )

        await self._training_repo.reset_definition(
            training_definition, command.delete_trainings
        )

        await self._repo.delete(training_definition)
