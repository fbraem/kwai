"""Module that defines all dataclasses for the tables containing coaches."""
from dataclasses import dataclass

from kwai.core.db.table import Table
from kwai.core.domain.value_objects.name import Name
from kwai.modules.training.coaches.coach import CoachEntity, CoachIdentifier


@dataclass(kw_only=True, frozen=True, slots=True)
class PersonRow:
    """Represent a row of the persons table."""

    id: int
    lastname: str
    firstname: str


PersonsTable = Table("persons", PersonRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class CoachRow:
    """Represent a row of the coaches table."""

    id: int
    person_id: int
    active: int

    def create_entity(self, person_row: PersonRow) -> CoachEntity:
        """Create a coach entity from this row."""
        return CoachEntity(
            id_=CoachIdentifier(self.id),
            name=Name(first_name=person_row.firstname, last_name=person_row.lastname),
            active=self.active == 1,
        )


CoachesTable = Table("coaches", CoachRow)
