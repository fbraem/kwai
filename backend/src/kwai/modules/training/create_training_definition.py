"""Module for the use case "Create Training Definition"."""
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.training_definition_command import TrainingDefinitionCommand
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)

CreateTrainingDefinitionCommand = TrainingDefinitionCommand


class CreateTrainingDefinition:
    """Use case for creating a training definition."""

    def __init__(self, repo: TrainingDefinitionRepository, owner: Owner):
        """Initialize the use case.

        Args:
            repo: The repository used to create the training definition.
            owner: The user that executes this use case.
        """
        self._repo = repo
        self._owner = owner

    async def execute(
        self, command: CreateTrainingDefinitionCommand
    ) -> TrainingDefinitionEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.
        """
        training_definition = TrainingDefinitionEntity(
            name=command.name,
            description=command.description,
            weekday=Weekday(command.weekday),
            period=TimePeriod.create_from_string(
                start=command.start_time, end=command.end_time
            ),
            active=command.active,
            location=command.location,
            remark=command.remark,
            owner=self._owner,
        )
        return await self._repo.create(training_definition)
