"""Module for testing TimePeriod value object."""

from datetime import time, timedelta

from kwai.core.domain.value_objects.time_period import TimePeriod


def test_delta():
    """Test delta of a TimePeriod."""
    period = TimePeriod(start=time(hour=20), end=time(hour=21))

    assert period.delta == timedelta(hours=1), "The delta should be 1 hour"


def test_create_from_string():
    """Test creating a time period from strings."""
    period = TimePeriod.create_from_string("20:00")
    assert period.endless, "This period should not have an end time."
    assert period.start.hour == 20, "The hours should be 20"
    assert period.start.minute == 0, "The minutes should be 0"

    period = TimePeriod.create_from_string("20:00", "21:30")
    assert not period.endless, "This period should have an end time."
    assert period.end.hour == 21, "The hours should be 20"
    assert period.end.minute == 30, "The minutes should be 30"
