"""Module for testing the coach database repository."""

import pytest


pytestmark = pytest.mark.db


async def test_create_coach(make_coach_in_db, make_member_in_db):
    """Test creating a coach."""
    coach = await make_coach_in_db()
    assert coach is not None, "There should be a coach."
    assert coach.id is not None, "Coach id should be provided."
