"""Module for testing LocalTimestamp."""

from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp


def test_create_now():
    """Test the create_now factory method."""
    timestamp = LocalTimestamp.create_now()

    assert timestamp is not None, "There should be a timestamp."


def test_add_delta():
    """Test the add delta method."""
    timestamp = LocalTimestamp.create_now()
    new_timestamp = timestamp.add_delta(hours=1)

    assert (
        timestamp.timestamp.hour + 1 == new_timestamp.timestamp.hour
    ), "The difference in hour should be 1."


def test_create_with_delta():
    """Test the create_with_delta factory method."""
    timestamp = LocalTimestamp.create_with_delta(hours=1)

    assert timestamp is not None, "There should be a timestamp."
