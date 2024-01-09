"""Schemas for training(s)."""
from types import NoneType
from typing import Annotated

from pydantic import BaseModel, Field

from kwai.api.converter import MarkdownConverter
from kwai.api.schemas.resources import (
    CoachResourceIdentifier,
    TeamResourceIdentifier,
    TrainingDefinitionResourceIdentifier,
    TrainingResourceIdentifier,
)
from kwai.api.v1.trainings.schemas.team import TeamDocument, TeamResource
from kwai.api.v1.trainings.schemas.training_definition import (
    TrainingDefinitionDocument,
    TrainingDefinitionResource,
)
from kwai.core.json_api import Document, Relationship, ResourceData
from kwai.modules.training.trainings.training import TrainingEntity


class TrainingText(BaseModel):
    """Schema for the content of a training."""

    locale: str
    format: str
    title: str
    summary: str
    content: str | None
    original_summary: str | None
    original_content: str | None


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


class CoachAttributes(BaseModel):
    """Attributes for a coach JSON:API resource."""

    name: str


class CoachResource(CoachResourceIdentifier, ResourceData[CoachAttributes, NoneType]):
    """A JSON:API resource for a coach."""


class TrainingAttributes(BaseModel):
    """Attributes for training JSON:API resource."""

    texts: list[TrainingText]
    event: TrainingEvent
    remark: str
    coaches: list[TrainingCoach]


class TrainingRelationships(BaseModel):
    """Relationships of a training JSON:API resource."""

    coaches: Relationship[CoachResourceIdentifier]
    teams: Relationship[TeamResourceIdentifier]
    definition: Relationship[TrainingDefinitionResourceIdentifier]


class TrainingResource(
    TrainingResourceIdentifier, ResourceData[TrainingAttributes, TrainingRelationships]
):
    """A JSON:API resource for a training."""


TrainingInclude = Annotated[
    TeamResource | TrainingDefinitionResource | CoachResource,
    Field(discriminator="type"),
]


class TrainingDocument(Document[TrainingResource, TrainingInclude]):
    """A JSON:API document for one or more training resources."""

    @classmethod
    def create(cls, training: TrainingEntity) -> "TrainingDocument":
        """Create a training document from a training entity."""
        training_resource = TrainingResource(
            id=str(training.id),
            attributes=TrainingAttributes(
                texts=[
                    TrainingText(
                        locale=text.locale.value,
                        format=text.format.value,
                        title=text.title,
                        summary=MarkdownConverter().convert(text.summary),
                        content=MarkdownConverter().convert(text.content)
                        if text.content
                        else None,
                        original_summary=text.summary,
                        original_content=text.content,
                    )
                    for text in training.texts
                ],
                event=TrainingEvent(
                    start_date=str(training.period.start_date),
                    end_date=str(training.period.end_date),
                    location=training.location or "",
                    cancelled=training.cancelled,
                    active=training.active,
                ),
                remark=training.remark or "",
                coaches=[
                    TrainingCoach(
                        id=str(coach.coach.id),
                        head=coach.type == 1,
                        present=coach.present,
                        payed=coach.payed,
                    )
                    for coach in training.coaches
                ],
            ),
        )

        included: set[TrainingInclude] = set()

        training_resource.relationships = TrainingRelationships(
            coaches=Relationship[CoachResourceIdentifier](data=[]),
            teams=Relationship[TeamResourceIdentifier](data=[]),
            definition=Relationship[TrainingDefinitionResourceIdentifier](data=None),
        )

        for training_coach in training.coaches:
            training_resource.relationships.coaches.data.append(
                CoachResourceIdentifier(id=str(training_coach.coach.id))
            )
            included.add(
                CoachResource(
                    id=str(training_coach.coach.id),
                    attributes=CoachAttributes(name=str(training_coach.coach.name)),
                )
            )
        if training.definition:
            training_resource.relationships.definition = Relationship[
                TrainingDefinitionResourceIdentifier
            ](
                data=(
                    TrainingDefinitionResourceIdentifier(id=str(training.definition.id))
                )
            )
            training_definition_document = TrainingDefinitionDocument.create(
                training.definition
            )
            included.add(training_definition_document.data)
            included = included.union(training_definition_document.included)

        for team in training.teams:
            training_resource.relationships.teams.data.append(
                TeamResourceIdentifier(id=str(team.id))
            )
            team_document = TeamDocument.create(team)
            included.add(team_document.data)

        return TrainingDocument(data=training_resource, included=included)
