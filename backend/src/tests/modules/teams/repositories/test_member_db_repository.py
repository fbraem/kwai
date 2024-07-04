"""Module for testing the team member repository for a database."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.domain.value_objects import Birthdate
from kwai.modules.teams.repositories.member_db_repository import (
    MemberDbRepository,
)

pytestmark = pytest.mark.db


async def test_get_all(database: Database, make_member_in_db):
    """Test getting all members."""
    member = await make_member_in_db()
    repo = MemberDbRepository(database)
    members = {member.id: member async for member in repo.get_all()}
    assert members is not None
    assert member.id in members, "The member should be returned."


async def test_get_by_id(database: Database, make_member_in_db):
    """Test get member by its ids."""
    member = await make_member_in_db()
    repo = MemberDbRepository(database)
    query = repo.create_query()
    query.filter_by_id(member.id)
    member = await repo.get(query)
    assert member is not None


async def test_get_by_birthdate(
    database: Database,
    make_member,
    make_member_in_db,
    make_person_in_db,
    make_person,
    make_contact_in_db,
    make_country_in_db,
    country_japan,
):
    """Test get a member by its birthdate."""
    birthdate = Birthdate(Date.create(year=2000, month=12, day=31))
    await make_member_in_db(
        make_member(
            person=await make_person_in_db(
                make_person(
                    birthdate=birthdate,
                    contact=await make_contact_in_db(),
                    nationality=await make_country_in_db(country_japan),
                )
            )
        )
    )

    repo = MemberDbRepository(database)
    query = repo.create_query()
    query.filter_by_birthdate(birthdate.date)
    member = await repo.get(query)
    assert member is not None


async def test_get_by_birthdate_between_dates(
    database: Database,
    make_member,
    make_member_in_db,
    make_person_in_db,
    make_person,
    make_contact_in_db,
    make_country_in_db,
    country_japan,
):
    """Test get a member by its birthdate between two dates."""
    birthdate = Birthdate(Date.create(year=1990, month=1, day=1))
    await make_member_in_db(
        make_member(
            person=await make_person_in_db(
                make_person(
                    birthdate=birthdate,
                    contact=await make_contact_in_db(),
                    nationality=await make_country_in_db(country_japan),
                )
            )
        )
    )
    repo = MemberDbRepository(database)
    query = repo.create_query()
    start_date = Date.create(year=1990, month=1, day=1)
    end_date = Date.create(year=1990, month=12, day=31)
    query.filter_by_birthdate(start_date, end_date)
    member = await repo.get(query)
    assert member is not None
