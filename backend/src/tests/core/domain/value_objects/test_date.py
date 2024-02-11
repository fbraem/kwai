"""Module for testing the Date value object."""
import datetime

from kwai.core.domain.value_objects.date import Date


def test_create_from_string():
    """Test the factory method create_from_string."""
    date = Date.create_from_string("1860-10-04")
    assert str(date) == "1860-10-04"


def test_create_with_year():
    """Test the factory method create with only a year."""
    date = Date.create(2024)
    assert date.year == 2024
    assert date.month == 1
    assert date.day == 1


def test_create():
    """Test the factory method create with all arguments."""
    date = Date.create(2024, 3, 9)
    assert date.year == 2024
    assert date.month == 3
    assert date.day == 9


def test_create_from_date():
    """Test the factory method to create a date from datetime.date."""
    date = Date.create_from_date(datetime.date.today())
    assert date.year == datetime.date.today().year
    assert date.month == datetime.date.today().month
    assert date.day == datetime.date.today().day


def test_day():
    """Test the day property."""
    date = Date.create_from_string("1860-10-04")
    assert date.day == 4


def test_month():
    """Test the year property."""
    date = Date.create_from_string("1860-10-04")
    assert date.month == 10


def test_year():
    """Test the year property."""
    date = Date.create_from_string("1860-10-04")
    assert date.year == 1860


def test_age():
    """Test age method."""
    birth_date = Date.create_from_string("1860-10-04")
    date_of_death = Date.create_from_string("1938-05-04")
    assert birth_date.get_age(date_of_death) == 77
