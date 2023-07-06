import pytest

from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.period import Period


def test_period_get_delta():
    """Test get_delta of a period."""
    period = Period(
        start_date=LocalTimestamp.create_now(),
        end_date=LocalTimestamp.create_with_delta(days=1),
    )

    assert period.get_delta().days == 1, "The period should be one day"


def test_wrong_period():
    """Test if a period fails when the end date is before the start date."""
    with pytest.raises(ValueError):
        Period(
            start_date=LocalTimestamp.create_now(),
            end_date=LocalTimestamp.create_with_delta(days=-1),
        )
