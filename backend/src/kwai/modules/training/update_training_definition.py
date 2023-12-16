"""Module for the use case "Update Training Definition"."""
from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.teams.team import TeamIdentifier
from kwai.modules.training.teams.team_repository import TeamRepository
from kwai.modules.training.training_definition_command import TrainingDefinitionCommand
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateTrainingDefinitionCommand(TrainingDefinitionCommand):
    """Input for the "Update Training Definition" use case."""

    id: int


class UpdateTrainingDefinition:
    """Use case for updating a training definition."""

    def __init__(
        self,
        repo: TrainingDefinitionRepository,
        team_repo: TeamRepository,
        owner: Owner,
    ):
        """Initialize the use case.

        Args:
            repo: The repository used to update the training definition.
            team_repo: A repository for getting the team.
            owner: The user that executes this use case.
        """
        self._repo = repo
        self._team_repo = team_repo
        self._owner = owner

    async def execute(
        self, command: UpdateTrainingDefinitionCommand
    ) -> TrainingDefinitionEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            TrainingDefinitionNotFoundException when the training definition does not
                exist.
        """
        if command.team_id is not None:
            team = await self._team_repo.get_by_id(TeamIdentifier(command.team_id))
        else:
            team = None
        training_definition = await self._repo.get_by_id(
            TrainingDefinitionIdentifier(command.id)
        )
        training_definition = Entity.replace(
            training_definition,
            name=command.name,
            description=command.description,
            weekday=Weekday(command.weekday),
            period=TimePeriod.create_from_string(
                start=command.start_time, end=command.end_time
            ),
            active=command.active,
            location=command.location,
            remark=command.remark,
            team=team,
            owner=self._owner,
        )
        await self._repo.update(training_definition)

        return training_definition
