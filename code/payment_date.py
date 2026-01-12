"""Payment date utilities.

Calculates payment dates with business day adjustments.
Provides configurable intervals and weekend handling.

"""

from datetime import datetime, timedelta
from typing import Optional


class PaymentDateConfig:
    """Configuration for payment date calculations."""
    DEFAULT_PAYMENT_INTERVAL_DAYS = 30
    SATURDAY = 5
    SUNDAY = 6
    DAYS_IN_WEEK = 7


class BusinessDayAdjuster:
    """Handles business day adjustments for dates."""
    
    @staticmethod
    def is_weekend(date: datetime) -> bool:
        """Check if a date falls on a weekend."""
        return date.weekday() >= PaymentDateConfig.SATURDAY
    
    @staticmethod
    def adjust_to_next_business_day(date: datetime) -> datetime:
        """Move date forward to next Monday if it falls on a weekend."""
        if not BusinessDayAdjuster.is_weekend(date):
            return date
        
        weekday = date.weekday()
        days_to_add = PaymentDateConfig.DAYS_IN_WEEK - weekday
        return date + timedelta(days=days_to_add)


class PaymentDate:
    """Provides utilities to compute future payment dates with business day handling."""
    
    def __init__(self, payment_interval_days: int = PaymentDateConfig.DEFAULT_PAYMENT_INTERVAL_DAYS):
        """Initialize with a configurable payment interval.
        
        Args:
            payment_interval_days: Number of days to add for payment calculation (default: 30)
        
        Raises:
            ValueError: If payment_interval_days is not positive
        """
        if payment_interval_days <= 0:
            raise ValueError("payment_interval_days must be positive")
        self._payment_interval_days = payment_interval_days
    
    def calculate_future_payment_date(self, starting_date: Optional[datetime]) -> datetime:
        """Calculate a payment date after the configured interval, adjusted to business days.
        
        Args:
            starting_date: The date to calculate from
            
        Returns:
            Payment date adjusted to next business day if needed
            
        Raises:
            ValueError: If starting_date is None
        """
        if starting_date is None:
            raise ValueError("starting_date cannot be None")
        
        calculated_date = starting_date + timedelta(days=self._payment_interval_days)
        return BusinessDayAdjuster.adjust_to_next_business_day(calculated_date)


def future_payment_date(starting_date: datetime) -> datetime:
    """Return a date 30 days after ``starting_date`` adjusted off weekends.
    
    Legacy function maintained for backward compatibility.
    Consider using PaymentDate class for new code.
    
    Args:
        starting_date: The date to calculate from
        
    Returns:
        Payment date 30 days in future, adjusted to next Monday if on weekend
    """
    payment_calculator = PaymentDate()
    return payment_calculator.calculate_future_payment_date(starting_date)
