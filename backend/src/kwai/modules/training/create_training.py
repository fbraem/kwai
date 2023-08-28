"""Module for the use case "Create training"."""
from dataclasses import dataclass
from typing import Any

from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import LocaleText
from kwai.modules.training.coaches.coach import CoachIdentifier
from kwai.modules.training.coaches.coach_repository import CoachRepository
from kwai.modules.training.trainings.training import TrainingEntity
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)
from kwai.modules.training.trainings.training_repository import TrainingRepository
from kwai.modules.training.trainings.value_objects import TrainingCoach


@dataclass(kw_only=True, frozen=True, slots=True)
class Coach:
    """Input for a coach associated with a training."""

    id: int
    head: bool = False
    present: bool = False
    payed: bool = False


@dataclass(kw_only=True, frozen=True, slots=True)
class CreateTrainingCommand:
    """Input for the "Create training" use case."""

    start_date: str
    end_date: str
    active: bool
    cancelled: bool
    location: str
    text: list[dict[str, Any]]
    remark: str
    definition: int | None
    coaches: list[Coach]
    teams: list[int]


class CreateTraining:
    """Use case for creating a training."""

    def __init__(
        self,
        repo: TrainingRepository,
        definition_repo: TrainingDefinitionRepository,
        coach_repo: CoachRepository,
        owner: Owner,
    ):
        """Initialize the use case.

        Args:
            repo: The repository used to create the training.
            definition_repo: The repository for getting the training definition.
            coach_repo: The repository for getting the coaches.
            owner: The user that executes this use case.
        """
        self._repo = repo
        self._definition_repo = definition_repo
        self._coach_repo = coach_repo
        self._owner = owner

    async def execute(self, command: CreateTrainingCommand) -> TrainingEntity:
        """Executes the use case.

        Args:
            command: The input for this use case.

        Raises:
            TrainingDefinitionNotFoundException: Raised when a training definition
                cannot be found.
        """
        if command.definition:
            definition = self._definition_repo.get_by_id(
                TrainingDefinitionIdentifier(command.definition)
            )
        else:
            definition = None

        if command.teams:
            teams = []
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

        training = TrainingEntity(
            content=[
                LocaleText(
                    locale=text["locale"],
                    format=text["format"],
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

        return await self._repo.create(training)
