"""Module for defining common JSON:API schemas."""

from typing import Self

from pydantic import BaseModel

from kwai.api.v1.resources import CountryResourceIdentifier
from kwai.core.json_api import Document, ResourceData
from kwai.modules.club.domain.country import CountryEntity


class CountryAttributes(BaseModel):
    """Attributes for the country JSON:API resource."""

    iso_2: str
    iso_3: str
    name: str


class CountryResource(CountryResourceIdentifier, ResourceData[CountryAttributes, None]):
    """A JSON:API resource for a country."""


class CountryDocument(Document[CountryResource, None]):
    """A JSON:API document for one or more countries."""

    @classmethod
    def create(cls, country: CountryEntity) -> Self:
        """Create a country document from a country value object."""
        country_resource = CountryResource(
            id=str(country.id),
            attributes=CountryAttributes(
                iso_2=country.iso_2, iso_3=country.iso_3, name=country.name
            ),
        )
        return cls(data=country_resource)
