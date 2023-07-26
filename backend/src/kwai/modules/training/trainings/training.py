"""Module for defining a training entity."""
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import LocaleText
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
)

TrainingIdentifier = IntIdentifier


class TrainingEntity(Entity[TrainingIdentifier]):
    """A training entity."""

    def __init__(
        self,
        *,
        id_: TrainingIdentifier | None = None,
        content: list[LocaleText],
        definition: TrainingDefinitionEntity | None,
        season: None = None,
        period: Period,
        active: bool = True,
        cancelled: bool = False,
        location: str = "",
        remark: str = "",
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize a training.

        Args:
            id_: The id of the training
            content: A list with text content
            definition: The related definition, when the training was created from a
                definition.
            period: The period of the training.
            season: The season that the training belongs to (not supported yet).
            active: Is this training active?
            cancelled: Is this training cancelled?
            location: The location of this training
            remark: A remark about this training
            traceable_time: The creation and modification timestamp of the training.
        """
        super().__init__(id_ or TrainingIdentifier())
        self._content = content
        self._definition = definition
        self._season = season
        self._period = period
        self._active = active
        self._cancelled = cancelled
        self._location = location
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def id(self) -> TrainingIdentifier:
        """Return the id of the training."""
        return self._id

    @property
    def definition(self) -> TrainingDefinitionEntity | None:
        """Return the related training definition."""
        return self._definition