"""Module that implements a MemberQuery for a database."""

from dataclasses import dataclass
from typing import Self

from sql_smith.functions import alias, criteria, func, group, literal, on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.members.member import MemberEntity, MemberIdentifier
from kwai.modules.club.members.member_query import MemberQuery
from kwai.modules.club.members.member_tables import (
    ContactRow,
    CountryRow,
    MemberRow,
    PersonRow,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberQueryRow(JoinedTableRow):
    """A data transfer object for the Member query."""

    member: MemberRow
    person: PersonRow
    nationality: CountryRow
    contact: ContactRow
    country: CountryRow

    def create_entity(self) -> MemberEntity:
        """Create a Member entity from a row."""
        return self.member.create_entity(
            person=self.person.create_entity(
                nationality=self.nationality.create_country(),
                contact=self.contact.create_entity(
                    country=self.country.create_country()
                ),
            )
        )


class MemberDbQuery(MemberQuery, DatabaseQuery):
    """A database query for members."""

    def __init__(self, database: Database):
        super().__init__(database)

    @property
    def count_column(self):
        return MemberRow.column("id")

    def init(self):
        self._query.from_(MemberRow.__table_name__).inner_join(
            PersonRow.__table_name__,
            on(PersonRow.column("id"), MemberRow.column("person_id")),
        ).inner_join(
            alias(CountryRow.__table_name__, "nationality"),
            on(
                "nationality.id",
                PersonRow.column("nationality_id"),
            ),
        ).inner_join(
            ContactRow.__table_name__,
            on(ContactRow.column("id"), PersonRow.column("contact_id")),
        ).inner_join(
            CountryRow.__table_name__,
            on(CountryRow.column("id"), ContactRow.column("country_id")),
        )

    @property
    def columns(self):
        return MemberQueryRow.get_aliases()

    def filter_by_id(self, id_: MemberIdentifier) -> Self:
        self._query.and_where(MemberRow.field("id").eq(id_.value))
        return self

    def filter_by_license(self, license: str) -> Self:
        self._query.and_where(MemberRow.field("license").eq(license))
        return self

    def filter_by_license_date(
        self, license_end_month: int, license_end_year: int
    ) -> Self:
        condition = criteria(
            "{} = {}",
            func("YEAR", MemberRow.column("license_end_date")),
            literal(license_end_year),
        ).and_(
            criteria(
                "{} = {}",
                func("MONTH", MemberRow.column("license_end_date")),
                literal(license_end_month),
            ),
        )
        self._query.and_where(group(condition))
        return self

    def filter_by_active(self) -> Self:
        self._query.and_where(MemberRow.field("active").eq(1))
        return self

    def filter_by_uuid(self, uuid: UniqueId) -> Self:
        self._query.and_where(MemberRow.field("uuid").eq(str(uuid)))
        return self
