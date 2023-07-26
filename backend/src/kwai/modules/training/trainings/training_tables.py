"""Module that defines all dataclasses for the tables containing trainings."""

from dataclasses import dataclass
from datetime import datetime, time

from kwai.core.db.table import Table
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.trainings.training import (
    TrainingEntity,
    TrainingIdentifier,
)
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.value_objects import Season


@dataclass(kw_only=True, frozen=True, slots=True)
class OwnerRow:
    """Represent the owner data."""

    id: int
    uuid: str
    first_name: str
    last_name: str

    def create_owner(self) -> Owner:
        """Create an Author value object from row data."""
        return Owner(
            id=IntIdentifier(self.id),
            uuid=UniqueId.create_from_string(self.uuid),
            name=Name(first_name=self.first_name, last_name=self.last_name),
        )


OwnersTable = Table("users", OwnerRow)


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
        definition: TrainingDefinitionEntity | None = None,
        season: Season | None = None,
    ) -> TrainingEntity:
        """Create a training entity from the table row.

        Returns:
            A training entity.
        """
        return TrainingEntity(
            id_=TrainingIdentifier(self.id),
            definition=definition,
            season=season,
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
        return TrainingRow(id=training.id.value)


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