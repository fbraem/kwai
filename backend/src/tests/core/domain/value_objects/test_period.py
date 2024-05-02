"""Module for testing the value object Period."""

import datetime

import pytest

from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.timestamp import Timestamp


def test_period_delta():
    """Test get_delta of a period."""
    period = Period(
        start_date=Timestamp.create_now(),
        end_date=Timestamp.create_with_delta(days=1),
    )

    assert period.delta.days == 1, "The period should be one day"


def test_initialize_period():
    """Test the initialization of a period."""
    period = Period(
        start_date=Timestamp(timestamp=datetime.datetime(1, 1, 1, 20, 0)),
        end_date=Timestamp(timestamp=datetime.datetime(1, 1, 1, 21, 0)),
    )
    assert (
        period.delta.total_seconds() / (60 * 60) == 1
    ), "The period should be one hour"


def test_wrong_period():
    """Test if a period fails when the end date is before the start date."""
    with pytest.raises(ValueError):
        Period(
            start_date=Timestamp.create_now(),
            end_date=Timestamp.create_with_delta(days=-1),
        )


def test_create_with_delta():
    """Test the create_with_delta factory method."""
    period = Period.create_from_delta(hours=1)

    assert (
        period.delta.total_seconds() / (60 * 60) == 1
    ), "The period should be one hour"
