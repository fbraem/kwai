"""Module for testing the team member repository for a database."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.domain.value_objects import Birthdate
from kwai.modules.club.repositories.team_member_db_repository import (
    TeamMemberDbRepository,
)

pytestmark = pytest.mark.db


async def test_get_all(database: Database, make_member_in_db):
    """Test getting all team members."""
    member = await make_member_in_db()
    repo = TeamMemberDbRepository(database)
    team_members = {team_member.id: team_member async for team_member in repo.get_all()}
    assert team_members is not None
    assert member.id in team_members, "The team member should be returned."


async def test_get_by_id(database: Database, make_member_in_db):
    """Test get team member by its ids."""
    member = await make_member_in_db()
    repo = TeamMemberDbRepository(database)
    query = repo.create_query()
    query.find_by_id(member.id)
    team_member = await repo.get(query)
    assert team_member is not None


async def test_get_by_birthdate(
    database: Database,
    make_member_in_db,
    make_person_in_db,
    make_person,
    make_contact_in_db,
):
    """Test get a member by its birthdate."""
    birthdate = Birthdate(Date.create(year=2000, month=12, day=31))
    await make_person_in_db(
        make_person(birthdate=birthdate, contact=await make_contact_in_db())
    )
    repo = TeamMemberDbRepository(database)
    query = repo.create_query()
    query.find_by_birthdate(birthdate.date)
    team_member = await repo.get(query)
    assert team_member is not None
