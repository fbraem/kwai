"""Module for testing the Weekday value object."""

from datetime import datetime, timedelta

import pytest

from kwai.core.domain.value_objects.weekday import Weekday


def first_monday(year, month):
    """Get the first monday of a month."""
    day = (8 - datetime(year, month, 1).weekday()) % 7
    return datetime(year, month, day)


@pytest.mark.parametrize(
    "test_input, result",
    [
        (first_monday(2023, 1), Weekday.MONDAY),
        (first_monday(2023, 1) + timedelta(days=1), Weekday.TUESDAY),
        (first_monday(2023, 1) + timedelta(days=2), Weekday.WEDNESDAY),
        (first_monday(2023, 1) + timedelta(days=3), Weekday.THURSDAY),
        (first_monday(2023, 1) + timedelta(days=4), Weekday.FRIDAY),
        (first_monday(2023, 1) + timedelta(days=5), Weekday.SATURDAY),
        (first_monday(2023, 1) + timedelta(days=6), Weekday.SUNDAY),
    ],
)
def test_create_weekday(test_input, result):
    """Test the creation of a weekday."""
    weekday = Weekday.create_from_date(test_input)

    assert weekday == result, "This weekday should be a monday"
