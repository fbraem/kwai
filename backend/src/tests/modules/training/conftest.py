"""Module with fixtures for the training bounded context."""
import dataclasses
from collections import defaultdict
from datetime import datetime
from typing import Any

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import LocaleText
from kwai.modules.training.coaches.coach_tables import (
    CoachesTable,
    CoachRow,
    PersonRow,
    PersonsTable,
)
from kwai.modules.training.teams.team_tables import TeamRow, TeamsTable
from kwai.modules.training.trainings.training import TrainingEntity

Context = dict[str, list[Any]]


@pytest.fixture(scope="module")
def context() -> Context:
    """A fixture for creating a context.

    This context is a dictionary for collecting data.
    """
    return defaultdict(list)


@pytest.fixture(scope="module")
def person_row() -> PersonRow:
    """Fixture for creating a person row."""
    return PersonRow(id=0, firstname="Jigoro", lastname="Kano")


@pytest.fixture(scope="module", autouse=True)
async def seed_persons(database: Database, person_row: PersonRow, context: Context):
    """Seed the database with persons."""
    # For now, we create the query, in the future a repository from the members
    # bounded context can be used.
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
def coach_row(seed_persons, context: Context) -> CoachRow:
    """Fixture for creating a coach row."""
    return CoachRow(id=0, person_id=context["persons"][0].id, active=True)


@pytest.fixture(scope="module", autouse=True)
async def seed_coaches(database: Database, coach_row: CoachRow, context: Context):
    """Seed the database with coaches."""
    query = database.create_query_factory().insert(CoachesTable.table_name)
    coach_dict = dataclasses.asdict(coach_row)
    del coach_dict["id"]
    query.columns(*coach_dict.keys()).values(*coach_dict.values())
    context["coaches"].append(
        dataclasses.replace(coach_row, id=await database.execute(query))
    )
    await database.commit()


@pytest.fixture(scope="module", autouse=True)
async def seed_teams(database: Database, context: Context):
    """Seed the database with teams."""
    query = database.create_query_factory().insert(TeamsTable.table_name)
    team_row = TeamRow(id=0, name="U18")
    team_dict = dataclasses.asdict(team_row)
    del team_dict["id"]
    query.columns(*team_dict.keys()).values(*team_dict.values())
    context["teams"].append(
        dataclasses.replace(team_row, id=await database.execute(query))
    )
    await database.commit()


@pytest.fixture
async def training_entity(training_repo, owner: Owner) -> TrainingEntity:
    """A fixture for a training entity."""
    start_date = LocalTimestamp.create_now()
    training = TrainingEntity(
        content=[
            LocaleText(
                locale="nl",
                format="md",
                title="Test Training",
                content="This is a test training",
                summary="This is a test training",
                author=owner,
            )
        ],
        period=Period(start_date=start_date, end_date=start_date.add_delta(hours=1)),
    )
    return training
