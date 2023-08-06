"""Module that defines all dataclasses for the tables containing trainings."""

from dataclasses import dataclass
from datetime import datetime, time

from kwai.core.db.rows import ContentRow
from kwai.core.db.table import Table
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import LocaleText
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.trainings.training import (
    TrainingEntity,
    TrainingIdentifier,
)
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.value_objects import Coach, Team, TrainingCoach


@dataclass(kw_only=True, frozen=True, slots=True)
class TrainingContentRow(ContentRow):
    """Represent a row in the training_contents table.

    Attributes:
        training_id: The id of the training
    """

    training_id: int

    @classmethod
    def persist(cls, training: TrainingEntity, content: LocaleText):
        """Persist a content value object to this table.

        Args:
            training: The training that contains the text content.
            content: The text content of the training.
        """
        return TrainingContentRow(
            training_id=training.id.value,
            locale=content.locale,
            format=content.format,
            title=content.title,
            content=content.content,
            summary=content.summary,
            user_id=content.author.id.value,
            created_at=content.traceable_time.created_at.timestamp,
            updated_at=content.traceable_time.updated_at.timestamp,
        )


TrainingContentsTable = Table("training_contents", TrainingContentRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class TrainingRow:
    """Represent a table row of the trainings table.

    Attributes:
        id: the id of the training
        definition_id: the id of the relation training definition
        season_id: the id of the related season
        created_at: the timestamp of creation
        updated_at: the timestamp of the last modification
        start_date: the timestamp of the start of the training
        end_date: the timestamp of the end of the training
        active: is this training active?
        cancelled: is this training cancelled?
        location: the location of the training
        remark: a remark about the training
    """

    id: int
    definition_id: int | None
    season_id: int | None
    created_at: datetime
    updated_at: datetime | None
    start_date: datetime
    end_date: datetime
    active: int
    cancelled: int
    location: str | None
    remark: str | None

    def create_entity(
        self,
        content: list[LocaleText],
        definition: TrainingDefinitionEntity | None = None,
    ) -> TrainingEntity:
        """Create a training entity from the table row.

        Returns:
            A training entity.
        """
        return TrainingEntity(
            id_=TrainingIdentifier(self.id),
            content=content,
            definition=definition,
            period=Period(
                start_date=LocalTimestamp(self.start_date),
                end_date=LocalTimestamp(self.end_date),
            ),
            active=self.active == 1,
            cancelled=self.cancelled == 1,
            location=self.location,
            remark=self.remark,
            traceable_time=TraceableTime(
                created_at=LocalTimestamp(self.created_at),
                updated_at=LocalTimestamp(self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, training: TrainingEntity) -> "TrainingRow":
        """Persist a training.

        Args:
            training: The training to persist.

        Returns:
            A dataclass containing the table row data.
        """
        return TrainingRow(
            id=training.id.value,
        )


TrainingsTable = Table("trainings", TrainingRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class TrainingDefinitionRow:
    """Represent a table row of the training definitions table."""

    id: int
    name: str
    description: str
    season_id: int | None
    team_id: int | None
    weekday: int
    start_time: time
    end_time: time
    active: int
    location: str | None
    remark: str | None
    user_id: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, owner: Owner) -> TrainingDefinitionEntity:
        """Create a training definition entity from a table row.

        Args:
            owner: The owner of the training definition.

        Returns:
            A training definition entity.
        """
        return TrainingDefinitionEntity(
            id_=TrainingDefinitionIdentifier(self.id),
            name=self.name,
            description=self.description,
            weekday=Weekday(self.weekday),
            period=TimePeriod(
                start=self.start_time,
                end=self.end_time,
            ),
            active=self.active == 1,
            location=self.location or "",
            remark=self.remark or "",
            owner=owner,
            traceable_time=TraceableTime(
                created_at=LocalTimestamp(self.created_at),
                updated_at=LocalTimestamp(self.updated_at),
            ),
        )

    @classmethod
    def persist(
        cls, training_definition: TrainingDefinitionEntity
    ) -> "TrainingDefinitionRow":
        """Persist a training definition entity."""
        return TrainingDefinitionRow(
            id=training_definition.id.value,
            name=training_definition.name,
            description=training_definition.description,
            season_id=None,
            team_id=None,
            weekday=training_definition.weekday.value,
            start_time=training_definition.period.start,
            end_time=training_definition.period.end,
            active=1 if training_definition.active else 0,
            location=training_definition.location,
            remark=training_definition.remark,
            user_id=training_definition.owner.id.value,
            created_at=training_definition.traceable_time.created_at.timestamp,
            updated_at=training_definition.traceable_time.updated_at.timestamp,
        )


TrainingDefinitionsTable = Table("training_definitions", TrainingDefinitionRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class TrainingCoachRow:
    """Represent a row of the training_coaches table."""

    training_id: int
    coach_id: int
    coach_type: int
    present: int
    payed: int
    remark: str | None
    user_id: int
    created_at: datetime
    updated_at: datetime | None

    def create_coach(self, coach: Coach, owner: Owner) -> TrainingCoach:
        """Create a TrainingCoach value object."""
        return TrainingCoach(
            coach=coach,
            owner=owner,
            present=self.present == 1,
            type=self.coach_type,
            payed=self.payed == 1,
            remark="" if self.remark is None else self.remark,
        )


TrainingCoachesTable = Table("training_coaches", TrainingCoachRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class TrainingTeamRow:
    """Represent a row of the training_teams table."""

    training_id: int
    team_id: int
    created_at: datetime
    updated_at: datetime | None


TrainingTeamsTable = Table("training_teams", TrainingTeamRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamRow:
    """Represent a row of the teams table."""

    id: int
    name: str

    def create_team(self):
        """Create a Team value object of this row."""
        return Team(id=IntIdentifier(self.id), name=self.name)


TeamsTable = Table("teams", TeamRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class CoachRow:
    """Represent a row of the coaches table."""

    id: int
    person_id: int


CoachesTable = Table("coaches", CoachRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class PersonRow:
    """Represent a row of the persons table."""

    id: int
    lastname: str
    firstname: str


PersonsTable = Table("persons", PersonRow)
