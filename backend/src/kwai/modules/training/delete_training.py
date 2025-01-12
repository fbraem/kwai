"""Module that defines the use case "Delete Training"."""

from dataclasses import dataclass

from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_repository import TrainingRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class DeleteTrainingCommand:
    """Input for the use case DeleteTraining."""

    id: int


class DeleteTraining:
    """Use case for deleting a training."""

    def __init__(self, repo: TrainingRepository):
        """Initialize the use case.

        Args:
            repo: A repository for deleting the training.
        """
        self._repo = repo

    async def execute(self, command: DeleteTrainingCommand) -> None:
        """Execute the use case.

        Args:
            command: The input for the use case.

        Raises:
            TrainingNotFoundException: raised when the training does not exist.
        """
        training = await self._repo.get_by_id(TrainingIdentifier(command.id))
        await self._repo.delete(training)
