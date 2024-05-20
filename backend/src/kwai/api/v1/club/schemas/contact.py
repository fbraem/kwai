"""Module for defining the JSON:API resource for a contact."""

from typing import Annotated, Self

from pydantic import BaseModel, Field

from kwai.api.v1.club.schemas.country import (
    CountryDocument,
    CountryResource,
)
from kwai.api.v1.club.schemas.resources import (
    ContactResourceIdentifier,
    CountryResourceIdentifier,
)
from kwai.core.json_api import Document, Relationship, ResourceData, ResourceMeta
from kwai.modules.club.domain.contact import ContactEntity


class ContactAttributes(BaseModel):
    """Attributes for the contact JSON:API resource."""

    emails: list[str] = Field(default_factory=list)
    tel: str
    mobile: str
    address: str
    postal_code: str
    city: str
    county: str
    remark: str


class ContactRelationships(BaseModel):
    """Relationships for the contact JSON:API resource."""

    country: Relationship[CountryResourceIdentifier]


class ContactResource(
    ContactResourceIdentifier, ResourceData[ContactAttributes, ContactRelationships]
):
    """A JSON:API resource for a contact."""


ContactInclude = Annotated[CountryResource, Field(discriminator="type")]


class ContactDocument(Document[ContactResource, ContactInclude]):
    """A JSON:API document for one or more contact resources."""

    @classmethod
    def create(cls, contact: ContactEntity) -> Self:
        """Create a contact document from a contact entity."""
        country_document = CountryDocument.create(contact.address.country)

        contact_resource = ContactResource(
            id=str(contact.id),
            attributes=ContactAttributes(
                emails=[str(email) for email in contact.emails],
                tel=contact.tel,
                mobile=contact.mobile,
                address=contact.address.address,
                postal_code=contact.address.postal_code,
                city=contact.address.city,
                county=contact.address.county,
                remark=contact.remark,
            ),
            relationships=ContactRelationships(
                country=Relationship[CountryResourceIdentifier](
                    data=CountryResourceIdentifier(id=country_document.data.id)
                )
            ),
            meta=ResourceMeta(
                created_at=str(contact.traceable_time.created_at),
                updated_at=str(contact.traceable_time.updated_at),
            ),
        )

        included: set[CountryResource] = set()
        included.add(country_document.data)

        return cls(data=contact_resource, included=included)
