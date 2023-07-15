"""Module for testing TimePeriod value object."""

from datetime import time, timedelta

from kwai.core.domain.value_objects.time_period import TimePeriod


def test_delta():
    """Test delta of a TimePeriod."""
    period = TimePeriod(start=time(hour=20), end=time(hour=21))

    assert period.delta == timedelta(hours=1), "The delta should be 1 hour"
