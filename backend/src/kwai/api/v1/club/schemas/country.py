"""Module for defining the JSON:API resource for a country."""

from typing import Self

from pydantic import BaseModel

from kwai.api.v1.club.schemas.resources import CountryResourceIdentifier
from kwai.core.json_api import Document, ResourceData
from kwai.modules.club.members.value_objects import Country


class CountryAttributes(BaseModel):
    """Attributes for the country JSON:API resource."""

    iso_2: str
    iso_3: str


class CountryResource(CountryResourceIdentifier, ResourceData[CountryAttributes, None]):
    """A JSON:API resource for a country."""


class CountryDocument(Document[CountryResource, None]):
    """A JSON:API document for one or more countries."""

    @classmethod
    def create(cls, country: Country) -> Self:
        """Create a country document from a country value object."""
        country_resource = CountryResource(
            id=str(country.id),
            attributes=CountryAttributes(iso_2=country.iso_2, iso_3=country.iso_3),
        )
        return cls(data=country_resource)
