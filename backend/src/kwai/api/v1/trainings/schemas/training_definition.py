"""Module for the training definition schema."""

from pydantic import BaseModel

from kwai.api.schemas.resources import (
    TeamResourceIdentifier,
    TrainingDefinitionResourceIdentifier,
)
from kwai.api.v1.trainings.schemas.team import TeamAttributes, TeamResource
from kwai.core.json_api import Document, Relationship, ResourceData, ResourceMeta
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity


class TrainingDefinitionAttributes(BaseModel):
    """Attributes for a training definition JSON:API resource."""

    name: str
    description: str
    weekday: int
    start_time: str
    end_time: str
    timezone: str
    active: bool
    location: str
    remark: str | None = None


class TrainingDefinitionRelationships(BaseModel):
    """Relationships for a training definition JSON:API resource."""

    team: Relationship[TeamResourceIdentifier] | None = None


class TrainingDefinitionResource(
    TrainingDefinitionResourceIdentifier,
    ResourceData[
        TrainingDefinitionAttributes,
        TrainingDefinitionRelationships,
    ],
):
    """A JSON:API resource for a training definition."""


class TrainingDefinitionDocument(Document[TrainingDefinitionResource, TeamResource]):
    """A JSON:API document for one or more training definitions."""

    @classmethod
    def create(
        cls, training_definition: TrainingDefinitionEntity
    ) -> "TrainingDefinitionDocument":
        """Create a document from a training definition entity."""
        data = TrainingDefinitionResource(
            id=str(training_definition.id),
            meta=ResourceMeta(
                created_at=str(training_definition.traceable_time.created_at),
                updated_at=str(training_definition.traceable_time.updated_at),
            ),
            attributes=TrainingDefinitionAttributes(
                name=training_definition.name,
                description=training_definition.description,
                weekday=training_definition.weekday.value,
                start_time=str(training_definition.period.start),
                end_time=str(training_definition.period.end),
                timezone=training_definition.period.timezone,
                active=training_definition.active,
                location=training_definition.location,
                remark=training_definition.remark or "",
            ),
        )

        included: set[TeamResource] = set()
        if training_definition.team is not None:
            data.relationships = TrainingDefinitionRelationships(
                team=Relationship[TeamResourceIdentifier](
                    data=TeamResourceIdentifier(id=str(training_definition.team.id))
                )
            )
            included.add(
                TeamResource(
                    id=str(training_definition.team.id),
                    attributes=TeamAttributes(name=str(training_definition.team.name)),
                )
            )

        return TrainingDefinitionDocument(data=data, included=included)
