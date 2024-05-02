"""Module for testing LocalTimestamp."""

from kwai.core.domain.value_objects.timestamp import Timestamp


def test_create_now():
    """Test the create_now factory method."""
    timestamp = Timestamp.create_now()

    assert timestamp is not None, "There should be a timestamp."


def test_add_delta():
    """Test the add delta method."""
    timestamp = Timestamp.create_now()
    new_timestamp = timestamp.add_delta(hours=1)

    assert (
        timestamp.timestamp.hour + 1 == new_timestamp.timestamp.hour
    ), "The difference in hour should be 1."


def test_create_with_delta():
    """Test the create_with_delta factory method."""
    timestamp = Timestamp.create_with_delta(hours=1)

    assert timestamp is not None, "There should be a timestamp."


def test_create_from_string():
    """Test creating a local timestamp with a string."""
    timestamp = Timestamp.create_from_string("1969-03-09 09:00:00")
    assert timestamp is not None, "There should be a timestamp"
    assert timestamp.year == 1969, "The year should be 1969"
    assert timestamp.month == 3, "The month should be 3"
    assert timestamp.day == 9, "The day should be 9"
    assert timestamp.hours == 9, "The hour should be 9"
    assert timestamp.minutes == 0, "The minutes should be 0"
    assert timestamp.seconds == 0, "The seconds should be 0"
