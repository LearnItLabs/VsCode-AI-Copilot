import pytest
from datetime import datetime
from payment_date import future_payment_date


def test_future_payment_date_weekday_to_weekday():
    """Test that a weekday plus 30 days landing on a weekday returns correct date."""
    starting_date = datetime(2024, 1, 1)  # Monday
    result = future_payment_date(starting_date)
    expected = datetime(2024, 1, 31)  # Wednesday
    assert result == expected


def test_future_payment_date_lands_on_saturday():
    """Test that a date landing on Saturday is moved to Monday."""
    starting_date = datetime(2024, 1, 3)  # Wednesday
    result = future_payment_date(starting_date)
    # 30 days later is Feb 2, 2024 (Friday)
    expected = datetime(2024, 2, 2)  # Friday
    assert result == expected
    
    # Test case that actually lands on Saturday
    starting_date = datetime(2024, 1, 4)  # Thursday
    result = future_payment_date(starting_date)
    # 30 days later is Feb 3, 2024 (Saturday) -> should move to Feb 5 (Monday)
    expected = datetime(2024, 2, 5)  # Monday
    assert result == expected


def test_future_payment_date_lands_on_sunday():
    """Test that a date landing on Sunday is moved to Monday."""
    starting_date = datetime(2024, 1, 5)  # Friday
    result = future_payment_date(starting_date)
    # 30 days later is Feb 4, 2024 (Sunday) -> should move to Feb 5 (Monday)
    expected = datetime(2024, 2, 5)  # Monday
    assert result == expected


def test_future_payment_date_lands_on_friday():
    """Test that a date landing on Friday requires no adjustment."""
    starting_date = datetime(2024, 1, 3)  # Wednesday
    result = future_payment_date(starting_date)
    # 30 days later is Feb 2, 2024 (Friday)
    expected = datetime(2024, 2, 2)  # Friday
    assert result == expected
    assert result.weekday() == 4  # Friday


def test_future_payment_date_month_boundary():
    """Test calculation across month boundaries."""
    starting_date = datetime(2024, 3, 15)  # Mid-March
    result = future_payment_date(starting_date)
    expected_date = datetime(2024, 4, 15)  # 30 days later
    assert result == expected_date


def test_future_payment_date_year_boundary():
    """Test calculation across year boundaries."""
    starting_date = datetime(2023, 12, 15)  # December
    result = future_payment_date(starting_date)
    # 30 days later is Jan 14, 2024 (Sunday) -> should move to Jan 15 (Monday)
    expected = datetime(2024, 1, 15)  # Monday
    assert result == expected


def test_future_payment_date_leap_year():
    """Test calculation during leap year February."""
    starting_date = datetime(2024, 2, 1)  # Feb 1, 2024 (leap year)
    result = future_payment_date(starting_date)
    # 30 days later is March 2, 2024 (Saturday) -> should move to March 4 (Monday)
    expected = datetime(2024, 3, 4)  # Monday
    assert result == expected