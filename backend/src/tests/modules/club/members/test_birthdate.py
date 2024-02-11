"""Module for testing the Birthdate value object."""
import pendulum

from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.members.value_objects import Birthdate


def test_age():
    """Test the age property."""
    birthdate = Birthdate(date=Date.create_from_string("1860-10-04"))
    pendulum.travel_to(pendulum.datetime(year=2024, month=1, day=1))
    assert birthdate.age == 163


def test_get_age_in_year():
    """Test get age in year."""
    birthdate = Birthdate(date=Date.create_from_string("1860-10-04"))
    assert birthdate.get_age_in_year(1938) == 78
