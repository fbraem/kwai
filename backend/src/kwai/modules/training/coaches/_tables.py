"""Module that defines all dataclasses for the tables containing coaches."""

from dataclasses import dataclass

from kwai.core.db.table_row import TableRow


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberRow(TableRow):
    """Represent a row of the members table."""

    __table_name__ = "judo_members"

    id: int


@dataclass(kw_only=True, frozen=True, slots=True)
class PersonRow(TableRow):
    """Represent a row of the persons table."""

    __table_name__ = "persons"

    id: int
    lastname: str
    firstname: str


@dataclass(kw_only=True, frozen=True, slots=True)
class CoachRow(TableRow):
    """Represent a row of the coaches table."""

    __table_name__ = "coaches"

    id: int
    member_id: int
    active: int
