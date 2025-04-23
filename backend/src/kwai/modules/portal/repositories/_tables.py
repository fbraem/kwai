"""Module for defining data transfer objects between domain and database."""

from dataclasses import dataclass
from datetime import datetime
from typing import Self

from kwai.core.db.table_row import TableRow
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorEntity, AuthorIdentifier


@dataclass(kw_only=True, frozen=True, slots=True)
class UserRow(TableRow):
    """Represent a row in the users table."""

    __table_name__ = "users"

    id: int
    uuid: str


@dataclass(kw_only=True, frozen=True, slots=True)
class AuthorRow(TableRow):
    """Represent a row in the authors table."""

    __table_name__ = "authors"

    user_id: int
    name: str
    remark: str
    active: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, uuid: UniqueId) -> AuthorEntity:
        """Create an author entity from a table row."""
        return AuthorEntity(
            id=AuthorIdentifier(self.user_id),
            uuid=uuid,
            name=self.name,
            remark=self.remark,
            active=self.active == 1,
            traceable_time=TraceableTime(
                created_at=Timestamp.create_utc(timestamp=self.created_at),
                updated_at=Timestamp.create_utc(timestamp=self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, author: AuthorEntity) -> Self:
        """Transform an author entity into a table row."""
        return cls(
            user_id=author.id.value,
            name=author.name,
            remark=author.remark,
            active=1 if author.active else 0,
            created_at=author.traceable_time.created_at.timestamp,  # type: ignore
            updated_at=author.traceable_time.updated_at.timestamp,
        )
