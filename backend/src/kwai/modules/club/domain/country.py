"""Module that defines the Country entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime

CountryIdentifier = IntIdentifier


class CountryEntity(Entity[CountryIdentifier]):
    """A country entity."""

    def __init__(
        self,
        *,
        id_: CountryIdentifier | None = None,
        iso_2: str,
        iso_3: str,
        name: str,
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize the country entity.

        Args:
            id_: The identifier of the country.
            iso_2: The ISO 2 code of the country.
            iso_3: The ISO 3 code of the country.
            name: The name of the country.
            traceable_time: The creation/modification time of the entity.
        """
        super().__init__(id_ or CountryIdentifier())
        self._iso_2 = iso_2
        self._iso_3 = iso_3
        self._name = name
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def iso_2(self) -> str:
        """Return the iso_2."""
        return self._iso_2

    @property
    def iso_3(self) -> str:
        """Return the iso_3."""
        return self._iso_3

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    def __str__(self) -> str:
        """Returns a string representation (iso_2) of the country."""
        return self._iso_2
