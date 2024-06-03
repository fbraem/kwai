"""Module that defines all tables related to members."""

from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Self

from kwai.core.db.table_row import TableRow
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.coach import CoachEntity
from kwai.modules.club.domain.contact import ContactEntity, ContactIdentifier
from kwai.modules.club.domain.country import CountryEntity, CountryIdentifier
from kwai.modules.club.domain.file_upload import FileUploadEntity
from kwai.modules.club.domain.member import MemberEntity, MemberIdentifier
from kwai.modules.club.domain.person import PersonEntity, PersonIdentifier
from kwai.modules.club.domain.team import TeamEntity
from kwai.modules.club.domain.value_objects import (
    Address,
    Birthdate,
    Gender,
    License,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class CountryRow(TableRow):
    """Represent a row of the countries table.

    Attributes:
        id: The id of the country.
        iso_2: The ISO 2 code of the country.
        iso_3: The ISO 3 code of the country.
    """

    __table_name__ = "countries"

    id: int | None = None
    iso_2: str
    iso_3: str
    name: str
    created_at: datetime
    updated_at: datetime | None

    def create_country(self) -> CountryEntity:
        """Create a Country value object from the row.

        Returns:
            A country value object.
        """
        return CountryEntity(
            id_=CountryIdentifier(self.id),
            iso_2=self.iso_2,
            iso_3=self.iso_3,
            name=self.name,
        )

    @classmethod
    def persist(cls, country: CountryEntity):
        """Persist a country to this table.

        Args:
            country: The country to persist.
        """
        return cls(
            iso_2=country.iso_2,
            iso_3=country.iso_3,
            name=country.name,
            created_at=datetime.now(UTC),
            updated_at=None,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class FileUploadRow(TableRow):
    """Represents a row of the imports table.

    Attributes:
        id: The id of the fileupload.
        filename: The name of the uploaded file.
        user_id: The id of the user that uploaded the file.
        created_at: The timestamp of creation.
        updated_at: The timestamp of modification.
    """

    __table_name__ = "imports"

    id: int
    uuid: str
    filename: str
    remark: str
    preview: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def persist(cls, file_upload: FileUploadEntity) -> Self:
        """Persist a file upload entity to this table.

        Args:
            file_upload: The entity to persist.
        """
        return cls(
            id=file_upload.id.value,
            uuid=str(file_upload.uuid),
            filename=file_upload.filename,
            remark=file_upload.remark,
            preview=1 if file_upload.preview else 0,
            user_id=file_upload.owner.id.value,
            created_at=file_upload.traceable_time.created_at.timestamp,  # type: ignore[arg-type]
            updated_at=file_upload.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class ContactRow(TableRow):
    """Represents a row of the contacts table."""

    __table_name__ = "contacts"

    id: int
    email: str
    tel: str
    mobile: str
    address: str
    postal_code: str
    city: str
    county: str | None
    country_id: int
    remark: str | None
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, country: CountryEntity) -> ContactEntity:
        """Create a contact entity from a table row."""
        emails = [EmailAddress(email) for email in self.email.split(";")]
        return ContactEntity(
            id_=ContactIdentifier(self.id),
            emails=emails,
            tel=self.tel,
            mobile=self.mobile,
            remark=self.remark or "",
            address=Address(
                address=self.address,
                postal_code=self.postal_code,
                city=self.city,
                county=self.county or "",
                country=country,
            ),
        )

    @classmethod
    def persist(cls, contact: ContactEntity) -> Self:
        """Create a row from a contact entity."""
        return cls(
            id=contact.id.value,
            email=";".join([str(email) for email in contact.emails]),
            tel=contact.tel,
            mobile=contact.mobile,
            address=contact.address.address,
            postal_code=contact.address.postal_code,
            city=contact.address.city,
            county=contact.address.county,
            country_id=contact.address.country.id.value,
            remark=contact.remark,
            created_at=contact.traceable_time.created_at.timestamp,  # type: ignore[arg-type]
            updated_at=contact.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class PersonRow(TableRow):
    """Represents a row of the persons table."""

    __table_name__ = "persons"

    id: int
    lastname: str
    firstname: str
    gender: int
    birthdate: date
    remark: str | None
    user_id: int | None
    contact_id: int
    nationality_id: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(
        self, nationality: CountryEntity, contact: ContactEntity
    ) -> PersonEntity:
        """Create a person entity from a table row."""
        return PersonEntity(
            id_=PersonIdentifier(self.id),
            name=Name(last_name=self.lastname, first_name=self.firstname),
            gender=Gender(self.gender),
            birthdate=Birthdate(Date.create_from_date(self.birthdate)),
            remark=self.remark or "",
            contact=contact,
            traceable_time=TraceableTime(
                created_at=Timestamp(self.created_at),
                updated_at=Timestamp(self.updated_at),
            ),
            nationality=nationality,
        )

    @classmethod
    def persist(cls, person: PersonEntity) -> Self:
        """Create a row from a person entity."""
        return cls(
            id=person.id.value,
            lastname=person.name.last_name or "",
            firstname=person.name.first_name or "",
            gender=person.gender.value,
            birthdate=person.birthdate.date.date,
            remark=person.remark,
            user_id=None,
            contact_id=person.contact.id.value,
            nationality_id=person.nationality.id.value,
            created_at=person.traceable_time.created_at.timestamp,  # type: ignore[arg-type]
            updated_at=person.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberRow(TableRow):
    """Represents a row of the members table."""

    __table_name__ = "judo_members"

    id: int
    uuid: str
    license: str
    license_end_date: date
    person_id: int
    remark: str | None
    competition: int
    created_at: datetime
    updated_at: datetime | None
    active: int

    def create_entity(self, person: PersonEntity) -> MemberEntity:
        """Create a member entity of a table row."""
        return MemberEntity(
            id_=MemberIdentifier(self.id),
            uuid=UniqueId.create_from_string(self.uuid),
            license=License(
                number=self.license,
                end_date=Date.create_from_date(self.license_end_date),
            ),
            remark=self.remark or "",
            competition=self.competition == 1,
            active=self.active == 1,
            person=person,
            traceable_time=TraceableTime(
                created_at=Timestamp(self.created_at),
                updated_at=Timestamp(self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, member: MemberEntity) -> Self:
        """Create a row from the member entity."""
        return cls(
            id=member.id.value,
            uuid=str(member.uuid),
            license=member.license.number,
            license_end_date=member.license.end_date.date,
            person_id=member.person.id.value,
            remark=member.remark,
            competition=1 if member.is_competitive else 0,
            active=1 if member.is_active else 0,
            created_at=member.traceable_time.created_at.timestamp,  # type: ignore[arg-type]
            updated_at=member.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberUploadRow(TableRow):
    """Represents a row of the judo member imports table."""

    __table_name__ = "judo_member_imports"

    member_id: int
    import_id: int
    created_at: datetime

    @classmethod
    def persist(cls, upload: FileUploadEntity, member: MemberEntity) -> Self:
        return cls(
            member_id=member.id.value,
            import_id=upload.id.value,
            created_at=datetime.now(UTC),
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class CoachRow(TableRow):
    """Represents a row of the coach table."""

    __table_name__ = "coaches"

    id: int
    member_id: int
    description: str
    diploma: str
    active: int
    remark: str
    user_id: int | None
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def persist(cls, coach: CoachEntity) -> Self:
        return cls(
            id=coach.id.value,
            member_id=coach.member.id.value,
            description=coach.description,
            diploma=coach.diploma,
            active=1 if coach.is_active else 0,
            remark=coach.remark,
            user_id=None if coach.user is None else coach.user.id.value,
            created_at=coach.traceable_time.created_at.timestamp,  # type: ignore[arg-type]
            updated_at=coach.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamRow(TableRow):
    """Represents a row of the teams table."""

    __table_name__ = "teams"

    id: int
    name: str
    season_id: int | None
    team_category_id: int | None
    active: int
    remark: str
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def persist(cls, team: TeamEntity) -> Self:
        return cls(
            id=team.id.value,
            name=team.name,
            season_id=None,
            team_category_id=None,
            active=1 if team.is_active else 0,
            remark=team.remark,
            created_at=team.traceable_time.created_at.timestamp,  # type: ignore[arg-type]
            updated_at=team.traceable_time.updated_at.timestamp,
        )
