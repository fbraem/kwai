"""Module for defining the JSON:API resource for a member."""

from typing import Annotated, Self

from pydantic import BaseModel, Field

from kwai.api.v1.club.schemas.contact import ContactResource
from kwai.api.v1.club.schemas.country import CountryResource
from kwai.api.v1.club.schemas.person import (
    PersonDocument,
    PersonResource,
)
from kwai.api.v1.club.schemas.resources import (
    MemberResourceIdentifier,
    PersonResourceIdentifier,
)
from kwai.core.json_api import Document, Relationship, ResourceData, ResourceMeta
from kwai.modules.club.members.member import MemberEntity


class MemberAttributes(BaseModel):
    """Attributes for the member JSON:API resource."""

    uuid: str
    license_number: str
    license_end_date: str
    remark: str
    active: bool
    competition: bool


class MemberRelationships(BaseModel):
    """Relationships of a member JSON:API resource."""

    person: Relationship[PersonResourceIdentifier]


class MemberResource(
    MemberResourceIdentifier, ResourceData[MemberAttributes, MemberRelationships]
):
    """A JSON:API resource for a member."""


MemberInclude = Annotated[
    PersonResource | ContactResource | CountryResource, Field(discriminator="type")
]


class MemberDocument(Document[MemberResource, MemberInclude]):
    """A JSON:API document for one or more member resources."""

    @classmethod
    def create(cls, member: MemberEntity) -> Self:
        """Create a member document from a member entity."""
        person_document = PersonDocument.create(member.person)

        member_resource = MemberResource(
            id=str(member.id),
            attributes=MemberAttributes(
                uuid=str(member.uuid),
                license_number=member.license.number,
                license_end_date=str(member.license.end_date),
                remark=member.remark,
                active=member.is_active,
                competition=member.is_competitive,
            ),
            meta=ResourceMeta(
                created_at=str(member.traceable_time.created_at),
                updated_at=str(member.traceable_time.updated_at),
            ),
        )
        member_resource.relationships = MemberRelationships(
            person=Relationship[PersonResourceIdentifier](
                data=PersonResourceIdentifier(id=person_document.resource.id)
            )
        )
        included: set[MemberInclude] = set()
        included.add(person_document.resource)
        if person_document.included is not None:
            included = included.union(person_document.included)

        return cls(data=member_resource, included=included)
