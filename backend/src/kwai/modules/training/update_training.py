"""Module for defining the use case "Update Training"."""
from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.training.coaches.coach import CoachIdentifier
from kwai.modules.training.coaches.coach_repository import CoachRepository
from kwai.modules.training.teams.team import TeamIdentifier
from kwai.modules.training.teams.team_repository import TeamRepository
from kwai.modules.training.training_command import TrainingCommand
from kwai.modules.training.trainings.training import TrainingEntity, TrainingIdentifier
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)
from kwai.modules.training.trainings.training_repository import TrainingRepository
from kwai.modules.training.trainings.value_objects import TrainingCoach


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateTrainingCommand(TrainingCommand):
    """Input for the "Update Training" use case."""

    id: int


class UpdateTraining:
    """Use case for updating a training."""

    def __init__(
        self,
        repo: TrainingRepository,
        definition_repo: TrainingDefinitionRepository,
        coach_repo: CoachRepository,
        team_repo: TeamRepository,
        owner: Owner,
    ):
        """Initialize the use case.

        Args:
            repo: The repository used to create the training.
            definition_repo: The repository for getting the training definition.
            coach_repo: The repository for getting the coaches.
            team_repo: The repository for getting the teams.
            owner: The user that executes this use case.
        """
        self._repo = repo
        self._definition_repo = definition_repo
        self._coach_repo = coach_repo
        self._team_repo = team_repo
        self._owner = owner

    async def execute(self, command: UpdateTrainingCommand) -> TrainingEntity:
        """Executes the use case.

        Args:
            command: The input for this use case.

        Raises:
            TrainingDefinitionNotFoundException: Raised when a training definition
                cannot be found.
        """
        training = await self._repo.get_by_id(TrainingIdentifier(command.id))

        if command.definition:
            definition = self._definition_repo.get_by_id(
                TrainingDefinitionIdentifier(command.definition)
            )
        else:
            definition = None

        if command.teams:
            teams = [
                entity
                async for entity in self._team_repo.get_by_ids(
                    *[TeamIdentifier(team_id) for team_id in command.teams]
                )
            ]
        else:
            teams = []

        if command.coaches:
            coaches = [
                TrainingCoach(coach=coach, owner=self._owner)
                async for coach in self._coach_repo.get_by_ids(
                    *[CoachIdentifier(coach.id) for coach in command.coaches]
                )
            ]
        else:
            coaches = []

        training = Entity.replace(
            training,
            content=[
                LocaleText(
                    locale=Locale(text["locale"]),
                    format=DocumentFormat(text["format"]),
                    title=text["title"],
                    content=text["content"],
                    summary=text["summary"],
                    author=self._owner,
                )
                for text in command.text
            ],
            definition=definition,
            coaches=coaches,
            teams=teams,
            period=Period(
                start_date=LocalTimestamp.create_from_string(command.start_date),
                end_date=LocalTimestamp.create_from_string(command.end_date),
            ),
            active=command.active,
            cancelled=command.cancelled,
            location=command.location,
            remark=command.remark,
        )

        await self._repo.update(training)
        return training
