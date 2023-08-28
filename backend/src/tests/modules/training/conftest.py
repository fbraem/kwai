"""Module with fixtures for the training bounded context."""
import dataclasses
from collections import defaultdict
from datetime import datetime
from typing import Any

import pytest

from kwai.core.db.database import Database
from kwai.modules.training.coaches.coach_tables import (
    CoachesTable,
    CoachRow,
    PersonRow,
    PersonsTable,
)

Context = dict[str, list[Any]]


@pytest.fixture(scope="module")
def context() -> Context:
    """A fixture for creating a context.

    This context is a dictionary for collecting data.
    """
    return defaultdict(list)


@pytest.fixture(scope="module")
def make_person_row():
    """Factory fixture for creating a person row."""

    def make(firstname: str = "Jigoro", lastname="Kano") -> PersonRow:
        return PersonRow(id=0, firstname=firstname, lastname=lastname)

    return make


@pytest.fixture(scope="module", autouse=True)
async def seed_persons(database: Database, make_person_row, context: Context):
    """Seed the database with persons."""
    # For now, we create the query, in the future a repository from the members
    # bounded context can be used.
    person_row = make_person_row()
    query = database.create_query_factory().insert(PersonsTable.table_name)
    person_dict = dataclasses.asdict(person_row)
    del person_dict["id"]
    person_dict["gender"] = 1
    person_dict["birthdate"] = datetime(year=1860, month=12, day=10)
    person_dict["nationality_id"] = 1
    query.columns(*person_dict.keys()).values(*person_dict.values())
    context["persons"].append(
        dataclasses.replace(person_row, id=await database.execute(query))
    )
    await database.commit()


@pytest.fixture(scope="module")
def make_coach_row():
    """Factory fixture for creating a coach row."""

    def make(person_row: PersonRow, active: bool = True):
        return CoachRow(id=0, person_id=person_row.id, active=active)

    return make


@pytest.fixture(scope="module", autouse=True)
async def seed_coaches(database: Database, make_coach_row, context: Context):
    """Seed the database with coaches."""
    coach_row = make_coach_row(context["persons"][0])

    query = database.create_query_factory().insert(CoachesTable.table_name)
    coach_dict = dataclasses.asdict(coach_row)
    del coach_dict["id"]
    query.columns(*coach_dict.keys()).values(*coach_dict.values())
    context["coaches"].append(
        dataclasses.replace(coach_row, id=await database.execute(query))
    )
    await database.commit()
