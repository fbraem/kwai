"""Module for the use case get training."""

from dataclasses import dataclass

from kwai.modules.training.trainings.training import TrainingEntity, TrainingIdentifier
from kwai.modules.training.trainings.training_repository import TrainingRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetTrainingCommand:
    """Input for the get training use case.

    Attributes:
        id: the id of the training.
    """

    id: int


class GetTraining:
    """Use case to get a training."""

    def __init__(self, repo: TrainingRepository):
        """Initialize the use case.

        Attributes:
            repo: The repository for trainings.
        """
        self._repo = repo

    async def execute(self, command: GetTrainingCommand) -> TrainingEntity:
        """Execute the use case.

        Args:
            command: the input for this use case.

        Raises:
            TrainingNotFoundException: Raised when the training with the given id
                does not exist.

        Returns:
            A training entity.
        """
        return await self._repo.get_by_id(TrainingIdentifier(command.id))
