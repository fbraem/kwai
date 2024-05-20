"""Module for defining the JSON:API resource for a person."""

from typing import Annotated, Self

from pydantic import BaseModel, Field

from kwai.api.v1.club.schemas.contact import ContactDocument, ContactResource
from kwai.api.v1.club.schemas.country import CountryDocument, CountryResource
from kwai.api.v1.club.schemas.resources import (
    ContactResourceIdentifier,
    CountryResourceIdentifier,
    PersonResourceIdentifier,
)
from kwai.core.json_api import Document, Relationship, ResourceData, ResourceMeta
from kwai.modules.club.domain.person import PersonEntity


class PersonAttributes(BaseModel):
    """Attributes for the person JSON:API resource."""

    first_name: str
    last_name: str
    gender: int
    birthdate: str
    remark: str


class PersonRelationships(BaseModel):
    """Relationships of a person JSON:API resource."""

    contact: Relationship[ContactResourceIdentifier]
    nationality: Relationship[CountryResourceIdentifier]


class PersonResource(
    PersonResourceIdentifier, ResourceData[PersonAttributes, PersonRelationships]
):
    """A JSON:API resource for a person."""


PersonInclude = Annotated[
    ContactResource | CountryResource, Field(discriminator="type")
]


class PersonDocument(Document[PersonResource, PersonInclude]):
    """A JSON:API document for one ore more persons."""

    @classmethod
    def create(cls, person: PersonEntity) -> Self:
        """Create a person document from a person entity."""
        country_document = CountryDocument.create(person.nationality)
        contact_document = ContactDocument.create(person.contact)

        person_resource = PersonResource(
            id=str(person.id),
            attributes=PersonAttributes(
                first_name=person.name.first_name,
                last_name=person.name.last_name,
                gender=person.gender.value,
                birthdate=str(person.birthdate),
                remark=person.remark,
            ),
            relationships=PersonRelationships(
                nationality=Relationship[CountryResourceIdentifier](
                    data=CountryResourceIdentifier(id=country_document.data.id)
                ),
                contact=Relationship[ContactResourceIdentifier](
                    data=ContactResourceIdentifier(id=contact_document.data.id)
                ),
            ),
            meta=ResourceMeta(
                created_at=str(person.traceable_time.created_at),
                updated_at=str(person.traceable_time.updated_at),
            ),
        )

        included: set[PersonInclude] = set()
        included.add(country_document.data)
        included.add(contact_document.data)
        included = included.union(contact_document.included)

        return PersonDocument(data=person_resource, included=included)
