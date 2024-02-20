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


def test_birth_date():
    """Test birthdate creating from a string."""
    birthdate = Birthdate(date=Date.create_from_string("1959-08-11"))
    assert birthdate.date.year == 1959
    assert birthdate.date.month == 8
    assert birthdate.date.day == 11
    assert str(birthdate) == "1959-08-11"
