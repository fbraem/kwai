"""Module for the training definition schema."""
from kwai.api.v1.trainings.schemas.team import TeamResource
from kwai.core import json_api
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity


@json_api.resource(type_="training_definitions")
class TrainingDefinitionResource:
    """JSON:API resource for a training definition."""

    def __init__(self, training_definition: TrainingDefinitionEntity):
        """Initialize a training definition resource.

        Args:
            training_definition: the training definition entity that is
                transformed to a JSON:API resource.
        """
        self._training_definition = training_definition

    @json_api.id
    def get_id(self) -> str:
        """Return the id of the training definition."""
        return str(self._training_definition.id)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        """Get the name of the training definition."""
        return self._training_definition.name

    @json_api.attribute(name="description")
    def get_description(self) -> str:
        """Get the description of the training definition."""
        return self._training_definition.description

    @json_api.attribute(name="weekday")
    def get_weekday(self) -> int:
        """Get the week day of the training definition."""
        return self._training_definition.weekday.value

    @json_api.attribute(name="start_time")
    def get_start_time(self) -> str:
        """Get the start time of the training definition."""
        return str(self._training_definition.period.start)

    @json_api.attribute(name="end_time")
    def get_end_time(self) -> str | None:
        """Get the end time of the training definition."""
        if self._training_definition.period.end:
            return str(self._training_definition.period.end)
        return None

    @json_api.attribute(name="active")
    def get_active(self) -> bool:
        """Get if the training definition is active."""
        return self._training_definition.active

    @json_api.attribute(name="location")
    def get_location(self) -> str:
        """Get the location of the training definition."""
        return self._training_definition.location

    @json_api.attribute(name="remark")
    def get_remark(self) -> str | None:
        """Get the remark of the training definition."""
        return self._training_definition.remark

    @json_api.attribute(name="created_at")
    def get_created_at(self) -> str | None:
        """Get the timestamp of creation."""
        return str(self._training_definition.traceable_time.created_at)

    @json_api.attribute(name="updated_at")
    def get_updated_at(self) -> str | None:
        """Get the timestamp of the last update."""
        return str(self._training_definition.traceable_time.updated_at)

    @json_api.relationship(name="team")
    def get_team(self) -> TeamResource | None:
        """Get the teams of the training."""
        if self._training_definition.team:
            return TeamResource(self._training_definition.team)
        return None
