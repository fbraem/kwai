"""Module that defines an entity for a person."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.club.domain.contact import ContactEntity
from kwai.modules.club.domain.country import CountryEntity
from kwai.modules.club.domain.value_objects import Birthdate, Gender


PersonIdentifier = IntIdentifier


class PersonEntity(Entity[PersonIdentifier]):
    """A person entity."""

    def __init__(
        self,
        *,
        id_: PersonIdentifier | None = None,
        name: Name,
        gender: Gender,
        birthdate: Birthdate,
        nationality: CountryEntity,
        contact: ContactEntity,
        remark: str = "",
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize a person.

        Args:
            id_: The id of the person.
            name: The name of the person.
            gender: The gender of the person.
            birthdate: The birthdate of the person.
            nationality: The nationality of the person.
            contact: The related contact entity.
            remark: A remark about the person.
            traceable_time: The creation and modification timestamp of the training.
        """
        super().__init__(id_ or PersonIdentifier())
        self._name = name
        self._gender = gender
        self._birthdate = birthdate
        self._nationality = nationality
        self._contact = contact
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def name(self) -> Name:
        """Return the name of the person."""
        return self._name

    @property
    def gender(self) -> Gender:
        """Return the gender of the person."""
        return self._gender

    @property
    def birthdate(self) -> Birthdate:
        """Return the birthdate of the person."""
        return self._birthdate

    @property
    def remark(self) -> str:
        """Return the remark."""
        return self._remark

    @property
    def contact(self) -> ContactEntity:
        """Return the contact."""
        return self._contact

    @property
    def nationality(self) -> CountryEntity:
        """Return the nationality."""
        return self._nationality

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the traceable_time."""
        return self._traceable_time
