"""Module for testing the team db repository."""

import pytest

pytestmark = pytest.mark.db


async def test_create_team(make_team_in_db):
    """Test creating a team in the database."""
    team = await make_team_in_db()
    assert team is not None, "There should be a team in the database."
