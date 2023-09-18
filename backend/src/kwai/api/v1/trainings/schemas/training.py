"""Schemas for training(s)."""

from pydantic import BaseModel

from kwai.api.converter import MarkdownConverter
from kwai.api.v1.trainings.schemas.training_definition import TrainingDefinitionResource
from kwai.core import json_api
from kwai.modules.training.coaches.coach import CoachEntity
from kwai.modules.training.teams.team import TeamEntity
from kwai.modules.training.trainings.training import TrainingEntity


class TrainingContent(BaseModel):
    """Schema for the content of a training."""

    locale: str
    format: str
    title: str
    summary: str
    content: str | None
    html_summary: str | None
    html_content: str | None


class TrainingCoach(BaseModel):
    """Schema for coach/training specific information."""

    id: str
    head: bool
    present: bool
    payed: bool


class TrainingEvent(BaseModel):
    """Schema for the event information of a training."""

    start_date: str
    end_date: str
    location: str
    cancelled: bool
    active: bool


@json_api.resource(type_="training_coaches")
class CoachResource:
    """Represent a coach attached to a training."""

    def __init__(self, coach: CoachEntity):
        self._coach = coach

    @json_api.id
    def get_id(self) -> str:
        """Get the id of the coach."""
        return str(self._coach.id)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        """Get the name of the coach."""
        return str(self._coach.name)


@json_api.resource(type_="teams")
class TeamResource:
    """Represent a team."""

    def __init__(self, team: TeamEntity):
        self._team = team

    @json_api.id
    def get_id(self) -> str:
        """Return the id of the team."""
        return str(self._team.id)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        """Return the name of the team."""
        return self._team.name


@json_api.resource(type_="trainings")
class TrainingResource:
    """Represent a JSON:API resource for a training entity."""

    def __init__(self, training: TrainingEntity):
        """Initialize a training resource.

        Args:
            training: The training entity that is transformed into a JSON:API resource.
        """
        self._training = training

    @json_api.id
    def get_id(self) -> str:
        """Get the id of the training."""
        return str(self._training.id)

    @json_api.attribute(name="contents")
    def get_contents(self) -> list[TrainingContent]:
        """Get the content of the training."""
        return [
            TrainingContent(
                locale=content.locale.value,
                format=content.format.value,
                title=content.title,
                summary=content.summary,
                content=content.content,
                html_summary=MarkdownConverter().convert(content.summary),
                html_content=None
                if content.content is None
                else MarkdownConverter().convert(content.content),
            )
            for content in self._training.content
        ]

    @json_api.attribute(name="event")
    def get_event(self) -> TrainingEvent:
        """Get the event information from a training."""
        return TrainingEvent(
            start_date=str(self._training.period.start_date),
            end_date=str(self._training.period.end_date),
            location=self._training.location or "",
            cancelled=self._training.cancelled,
            active=self._training.active,
        )

    @json_api.attribute(name="remark")
    def get_remark(self) -> str:
        """Get the remark of the training."""
        return self._training.remark or ""

    @json_api.attribute(name="coaches")
    def get_training_coaches(self) -> list[TrainingCoach]:
        """Get a list with coach data."""
        return [
            TrainingCoach(
                id=training_coach.coach.id.value,
                head=training_coach.type == 1,
                present=training_coach.present,
                payed=training_coach.payed,
            )
            for training_coach in self._training.coaches
        ]

    @json_api.relationship(name="coaches")
    def get_coaches(self) -> list[CoachResource]:
        """Get the coaches attached to the training."""
        return [
            CoachResource(training_coach.coach)
            for training_coach in self._training.coaches
        ]

    @json_api.relationship(name="teams")
    def get_teams(self) -> list[TeamResource]:
        """Get the teams of the training."""
        return [TeamResource(team) for team in self._training.teams]

    @json_api.relationship(name="definition")
    def get_definition(self) -> TrainingDefinitionResource | None:
        """Get the related training definition resource."""
        definition = self._training.definition
        if definition:
            return TrainingDefinitionResource(definition)
        return None

    @json_api.attribute(name="created_at")
    def get_created_at(self) -> str | None:
        """Get the timestamp of creation."""
        return str(self._training.traceable_time.created_at)

    @json_api.attribute(name="updated_at")
    def get_updated_at(self) -> str | None:
        """Get the timestamp of the last update."""
        return str(self._training.traceable_time.updated_at)
