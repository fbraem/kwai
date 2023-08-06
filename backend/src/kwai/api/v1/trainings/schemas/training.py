from pydantic import BaseModel

from kwai.api.converter import MarkdownConverter
from kwai.core import json_api
from kwai.modules.training.trainings.training import TrainingEntity
from kwai.modules.training.trainings.value_objects import TrainingCoach, Team


class TrainingContent(BaseModel):
    """Schema for the content of a training."""

    locale: str
    title: str
    summary: str
    content: str | None


@json_api.resource(type_="training_coaches")
class TrainingCoachResource:
    """Represent a coach attached to a training."""

    def __init__(self, training_coach: TrainingCoach):
        self._training_coach = training_coach

    @json_api.id
    def get_id(self) -> str:
        """Get the id of the coach."""
        return str(self._training_coach.coach.id)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        """Get the name of the coach."""
        return str(self._training_coach.coach.name)


@json_api.resource(type_="teams")
class TeamResource:
    """Represent a team."""

    def __init__(self, team: Team):
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

    @json_api.attribute(name="content")
    def get_content(self) -> list[TrainingContent]:
        """Get the content of the training."""
        return [
            TrainingContent(
                locale=content.locale,
                title=content.title,
                summary=MarkdownConverter().convert(content.summary),
                content=MarkdownConverter().convert(content.content)
                if content.content
                else None,
            )
            for content in self._training.content
        ]

    @json_api.relationship(name="coaches")
    def get_coaches(self) -> list[TrainingCoachResource]:
        """Get the coaches attached to the training."""
        return [
            TrainingCoachResource(training_coach)
            for training_coach in self._training.coaches
        ]

    @json_api.relationship(name="teams")
    def get_teams(self) -> list[TeamResource]:
        """Get the teams of the training."""
        return [TeamResource(team) for team in self._training.teams]
