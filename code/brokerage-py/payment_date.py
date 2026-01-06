"""Payment date utilities.

Calculates a payment date 30 days in the future from a provided
starting date and adjusts forward if the date falls on a weekend.

"""

from datetime import datetime, timedelta

def future_payment_date(starting_date: datetime) -> datetime:
    """Return a date 30 days after ``starting_date`` adjusted off weekends.

    If it lands on Saturday or Sunday, move it forward to Monday.
    """
    calculated_future_date = starting_date + timedelta(days=30)
    weekday = calculated_future_date.weekday()  # Monday=0 .. Sunday=6
    if weekday >= 5:  # weekend
        calculated_future_date = calculated_future_date + timedelta(days=(7 - weekday))
    return calculated_future_date


class PaymentDate:
    """Provides helpers to compute future payment dates with weekend handling."""
    def calculate_future_payment_date(self, starting_date: datetime) -> datetime:
        """Return a payment date 30 days after ``starting_date`` adjusted off weekends."""
        return future_payment_date(starting_date)
