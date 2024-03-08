"""Module for defining the JSON:API resource for a member."""

from typing import Annotated, Self

from pydantic import BaseModel, Field

from kwai.api.v1.club.schemas.contact import ContactAttributes, ContactResource
from kwai.api.v1.club.schemas.country import CountryResource
from kwai.api.v1.club.schemas.person import PersonAttributes, PersonResource
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
                data=PersonResourceIdentifier(id=str(member.person.id))
            )
        )
        included: set[MemberInclude] = set()
        included.add(
            PersonResource(
                id=str(member.person.id),
                attributes=PersonAttributes(
                    first_name=member.person.name.first_name,
                    last_name=member.person.name.last_name,
                    gender=member.person.gender.value,
                    birthdate=str(member.person.birthdate),
                    remark=member.person.remark,
                ),
                meta=ResourceMeta(
                    created_at=str(member.person.traceable_time.created_at),
                    updated_at=str(member.person.traceable_time.updated_at),
                ),
            )
        )
        included.add(
            ContactResource(
                id=str(member.person.contact.id),
                attributes=ContactAttributes(
                    emails=[str(email) for email in member.person.contact.emails],
                    tel=member.person.contact.tel,
                    mobile=member.person.contact.mobile,
                    address=member.person.contact.address.address,
                    postal_code=member.person.contact.address.postal_code,
                    city=member.person.contact.address.city,
                    county=member.person.contact.address.county,
                    remark=member.person.contact.remark,
                ),
            )
        )
