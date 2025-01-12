"""Module that defines the JSON:API schemas for coaches."""

from types import NoneType

from pydantic import BaseModel

from kwai.api.schemas.resources import CoachResourceIdentifier
from kwai.core.json_api import Document, ResourceData
from kwai.modules.training.coaches.coach import CoachEntity


class CoachAttributes(BaseModel):
    """Attributes for a coach JSON:API resource."""

    name: str


class CoachResource(CoachResourceIdentifier, ResourceData[CoachAttributes, NoneType]):
    """A JSON:API resource for a coach."""

    @classmethod
    def create(cls, coach: CoachEntity) -> "CoachResource":
        """Create a JSON:API resource from a coach entity."""
        return CoachResource(
            id=str(coach.id), attributes=CoachAttributes(name=str(coach.name))
        )


class CoachDocument(Document[CoachResource, NoneType]):
    """A JSON:API document for one or more coaches."""

    @classmethod
    def create(cls, coach: CoachEntity) -> "CoachDocument":
        """Create a document from a coach entity."""
        return CoachDocument(data=CoachResource.create(coach))
