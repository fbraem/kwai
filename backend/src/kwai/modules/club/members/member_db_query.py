"""Module that implements a MemberQuery for a database."""
from typing import Self

from sql_smith.functions import alias, on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.club.members.member import MemberIdentifier
from kwai.modules.club.members.member_query import MemberQuery
from kwai.modules.club.members.member_tables import (
    ContactsTable,
    CountriesTable,
    MembersTable,
    PersonsTable,
)


class MemberDbQuery(MemberQuery, DatabaseQuery):
    """A database query for members."""

    def __init__(self, database: Database):
        super().__init__(database)

    def init(self):
        self._query.from_(MembersTable.table_name).inner_join(
            PersonsTable.table_name,
            on(PersonsTable.column("id"), MembersTable.column("person_id")),
        ).inner_join(
            alias(CountriesTable.table_name, "nationalities"),
            on(
                "nationalities.id",
                PersonsTable.column("nationality_id"),
            ),
        ).inner_join(
            ContactsTable.table_name,
            on(ContactsTable.column("id"), PersonsTable.column("contact_id")),
        ).inner_join(
            CountriesTable.table_name,
            on(CountriesTable.column("id"), ContactsTable.column("country_id")),
        )

    @property
    def columns(self):
        return (
            MembersTable.aliases()
            + PersonsTable.aliases()
            + CountriesTable.aliases("nationalities")
            + ContactsTable.aliases()
            + CountriesTable.aliases()
        )

    def filter_by_id(self, id_: MemberIdentifier) -> Self:
        self._query.and_where(MembersTable.field("id").eq(id_.value))
        return self

    def filter_by_license(self, license: str) -> Self:
        self._query.and_where(MembersTable.field("license").eq(license))
        return self
