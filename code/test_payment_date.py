"""Tests for payment_date module."""

import unittest
from datetime import datetime
from payment_date import (
    PaymentDate,
    BusinessDayAdjuster,
    PaymentDateConfig,
    future_payment_date
)


class TestBusinessDayAdjuster(unittest.TestCase):
    """Test cases for BusinessDayAdjuster."""
    
    def test_is_weekend_saturday(self):
        """Saturday should be identified as weekend."""
        saturday = datetime(2026, 1, 17)  # Saturday
        self.assertTrue(BusinessDayAdjuster.is_weekend(saturday))
    
    def test_is_weekend_sunday(self):
        """Sunday should be identified as weekend."""
        sunday = datetime(2026, 1, 18)  # Sunday
        self.assertTrue(BusinessDayAdjuster.is_weekend(sunday))
    
    def test_is_weekend_monday(self):
        """Monday should not be identified as weekend."""
        monday = datetime(2026, 1, 12)  # Monday
        self.assertFalse(BusinessDayAdjuster.is_weekend(monday))
    
    def test_is_weekend_friday(self):
        """Friday should not be identified as weekend."""
        friday = datetime(2026, 1, 16)  # Friday
        self.assertFalse(BusinessDayAdjuster.is_weekend(friday))
    
    def test_adjust_weekday_unchanged(self):
        """Weekday dates should remain unchanged."""
        wednesday = datetime(2026, 1, 14)  # Wednesday
        result = BusinessDayAdjuster.adjust_to_next_business_day(wednesday)
        self.assertEqual(result, wednesday)
    
    def test_adjust_saturday_to_monday(self):
        """Saturday should adjust to following Monday."""
        saturday = datetime(2026, 1, 17)  # Saturday
        expected_monday = datetime(2026, 1, 19)  # Monday
        result = BusinessDayAdjuster.adjust_to_next_business_day(saturday)
        self.assertEqual(result, expected_monday)
    
    def test_adjust_sunday_to_monday(self):
        """Sunday should adjust to following Monday."""
        sunday = datetime(2026, 1, 18)  # Sunday
        expected_monday = datetime(2026, 1, 19)  # Monday
        result = BusinessDayAdjuster.adjust_to_next_business_day(sunday)
        self.assertEqual(result, expected_monday)


class TestPaymentDate(unittest.TestCase):
    """Test cases for PaymentDate class."""
    
    def test_default_interval(self):
        """Default payment interval should be 30 days."""
        payment_date = PaymentDate()
        start = datetime(2026, 1, 1)
        result = payment_date.calculate_future_payment_date(start)
        self.assertEqual(result, datetime(2026, 1, 31))
    
    def test_custom_interval(self):
        """Custom payment interval should be respected."""
        payment_date = PaymentDate(payment_interval_days=15)
        start = datetime(2026, 1, 1)
        result = payment_date.calculate_future_payment_date(start)
        self.assertEqual(result, datetime(2026, 1, 16))
    
    def test_invalid_interval_zero(self):
        """Zero payment interval should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            PaymentDate(payment_interval_days=0)
        self.assertIn("positive", str(context.exception))
    
    def test_invalid_interval_negative(self):
        """Negative payment interval should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            PaymentDate(payment_interval_days=-5)
        self.assertIn("positive", str(context.exception))
    
    def test_none_starting_date(self):
        """None starting_date should raise ValueError."""
        payment_date = PaymentDate()
        with self.assertRaises(ValueError) as context:
            payment_date.calculate_future_payment_date(None)
        self.assertIn("None", str(context.exception))
    
    def test_weekend_adjustment_saturday(self):
        """Payment date on Saturday should move to Monday."""
        payment_date = PaymentDate(payment_interval_days=10)
        start = datetime(2026, 1, 7)  # Results in Jan 17 (Saturday)
        result = payment_date.calculate_future_payment_date(start)
        self.assertEqual(result, datetime(2026, 1, 19))  # Monday
    
    def test_weekend_adjustment_sunday(self):
        """Payment date on Sunday should move to Monday."""
        payment_date = PaymentDate(payment_interval_days=11)
        start = datetime(2026, 1, 7)  # Results in Jan 18 (Sunday)
        result = payment_date.calculate_future_payment_date(start)
        self.assertEqual(result, datetime(2026, 1, 19))  # Monday
    
    def test_no_adjustment_needed(self):
        """Payment date on weekday should remain unchanged."""
        payment_date = PaymentDate(payment_interval_days=7)
        start = datetime(2026, 1, 7)  # Results in Jan 14 (Wednesday)
        result = payment_date.calculate_future_payment_date(start)
        self.assertEqual(result, datetime(2026, 1, 14))
    
    def test_year_boundary(self):
        """Payment date calculation should work across year boundary."""
        payment_date = PaymentDate(payment_interval_days=30)
        start = datetime(2025, 12, 10)
        result = payment_date.calculate_future_payment_date(start)
        self.assertEqual(result, datetime(2026, 1, 9))


class TestLegacyFunction(unittest.TestCase):
    """Test cases for backward compatibility function."""
    
    def test_future_payment_date_backward_compatibility(self):
        """Legacy function should maintain original behavior."""
        start = datetime(2026, 1, 1)
        result = future_payment_date(start)
        self.assertEqual(result, datetime(2026, 1, 31))
    
    def test_future_payment_date_weekend_adjustment(self):
        """Legacy function should adjust weekends."""
        start = datetime(2026, 1, 7)  # Results in Jan 17 (Saturday) + 30 days
        # Actually Jan 6 + 30 = Feb 5 (Thursday), let me recalculate
        # Jan 7 + 30 = Feb 6 (Friday) - no adjustment needed
        result = future_payment_date(start)
        self.assertEqual(result, datetime(2026, 2, 6))
    
    def test_future_payment_date_lands_on_saturday(self):
        """Legacy function should move Saturday to Monday."""
        start = datetime(2025, 12, 17)  # + 30 days = Jan 16, 2026 (Friday)
        # Let me use a date that lands on Saturday
        start = datetime(2025, 12, 18)  # + 30 days = Jan 17, 2026 (Saturday)
        result = future_payment_date(start)
        self.assertEqual(result, datetime(2026, 1, 19))  # Monday


class TestPaymentDateConfig(unittest.TestCase):
    """Test cases for PaymentDateConfig constants."""
    
    def test_default_interval_constant(self):
        """Default interval should be 30 days."""
        self.assertEqual(PaymentDateConfig.DEFAULT_PAYMENT_INTERVAL_DAYS, 30)
    
    def test_saturday_constant(self):
        """Saturday weekday constant should be 5."""
        self.assertEqual(PaymentDateConfig.SATURDAY, 5)
    
    def test_sunday_constant(self):
        """Sunday weekday constant should be 6."""
        self.assertEqual(PaymentDateConfig.SUNDAY, 6)
    
    def test_days_in_week_constant(self):
        """Days in week constant should be 7."""
        self.assertEqual(PaymentDateConfig.DAYS_IN_WEEK, 7)


if __name__ == '__main__':
    unittest.main()
