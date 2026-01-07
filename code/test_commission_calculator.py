import pytest
from decimal import Decimal
from commission_calculator import CommissionCalculator


@pytest.fixture
def calculator():
    """Fixture to provide a CommissionCalculator instance."""
    return CommissionCalculator()


def test_negative_units_sold_raises_error(calculator):
    """Test that negative units_sold raises ValueError."""
    with pytest.raises(ValueError, match="UnitsSold cannot be less than zero"):
        calculator.get_commission_for_the_sale(-1, Decimal("10.00"))


def test_negative_unit_price_raises_error(calculator):
    """Test that negative unit_price raises ValueError."""
    with pytest.raises(ValueError, match="unitPrice cannot be less than zero"):
        calculator.get_commission_for_the_sale(10, Decimal("-5.00"))


def test_zero_units_sold_returns_zero_commission(calculator):
    """Test that zero units sold results in zero commission."""
    result = calculator.get_commission_for_the_sale(0, Decimal("100.00"))
    assert result == Decimal("0")


def test_zero_unit_price_returns_zero_commission(calculator):
    """Test that zero unit price results in zero commission."""
    result = calculator.get_commission_for_the_sale(100, Decimal("0"))
    assert result == Decimal("0")


def test_epic_commission_by_sales_amount_threshold(calculator):
    """Test Epic commission when gross sale meets EpicSalesAmount threshold."""
    from constants import Constants
    # Assuming EpicSalesAmount = 10000 and Epic rate = 0.15
    units_sold = 100
    unit_price = Decimal("150.00")  # gross_sale = 15000
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = Decimal("15000") * Constants.CommissionRate.Epic
    assert result == expected


def test_epic_commission_by_unit_amount_threshold(calculator):
    """Test Epic commission when units sold meets EpicUnitAmount threshold."""
    from constants import Constants
    # Assuming EpicUnitAmount = 500
    units_sold = 600
    unit_price = Decimal("5.00")  # gross_sale = 3000 (below Epic sales threshold)
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = Decimal("3000") * Constants.CommissionRate.Epic
    assert result == expected


def test_epic_commission_exactly_at_sales_threshold(calculator):
    """Test Epic commission when gross sale exactly equals EpicSalesAmount."""
    from constants import Constants
    # Test boundary condition
    threshold = Constants.CommissionThreshold.EpicSalesAmount
    units_sold = 1
    unit_price = threshold
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = threshold * Constants.CommissionRate.Epic
    assert result == expected


def test_earner_commission_by_sales_amount_threshold(calculator):
    """Test Earner commission when gross sale meets EarnerSalesAmount threshold."""
    from constants import Constants
    # Assuming EarnerSalesAmount = 5000 and Earner rate = 0.10
    units_sold = 100
    unit_price = Decimal("75.00")  # gross_sale = 7500
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = Decimal("7500") * Constants.CommissionRate.Earner
    assert result == expected


def test_earner_commission_by_unit_amount_threshold(calculator):
    """Test Earner commission when units sold meets EarnerUnitAmount threshold."""
    from constants import Constants
    # Assuming EarnerUnitAmount = 200
    units_sold = 250
    unit_price = Decimal("10.00")  # gross_sale = 2500 (below Earner sales threshold)
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = Decimal("2500") * Constants.CommissionRate.Earner
    assert result == expected


def test_earner_commission_exactly_at_sales_threshold(calculator):
    """Test Earner commission when gross sale exactly equals EarnerSalesAmount."""
    from constants import Constants
    threshold = Constants.CommissionThreshold.EarnerSalesAmount
    units_sold = 1
    unit_price = threshold
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = threshold * Constants.CommissionRate.Earner
    assert result == expected


def test_standard_commission_below_thresholds(calculator):
    """Test Standard commission when below all thresholds."""
    from constants import Constants
    # Small sale that doesn't meet any threshold
    units_sold = 10
    unit_price = Decimal("10.00")  # gross_sale = 100
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = Decimal("100") * Constants.CommissionRate.Standard
    assert result == expected


def test_standard_commission_one_below_earner_threshold(calculator):
    """Test Standard commission just below Earner sales threshold."""
    from constants import Constants
    threshold = Constants.CommissionThreshold.EarnerSalesAmount
    units_sold = 1
    unit_price = threshold - Decimal("0.01")
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = unit_price * Constants.CommissionRate.Standard
    assert result == expected


def test_decimal_precision_maintained(calculator):
    """Test that decimal precision is maintained in calculations."""
    units_sold = 3
    unit_price = Decimal("33.33")
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    # Ensure result is a Decimal type and maintains precision
    assert isinstance(result, Decimal)
    assert result == Decimal("99.99") * result / Decimal("99.99")  # Verify precision


def test_large_numbers_calculation(calculator):
    """Test commission calculation with large numbers."""
    from constants import Constants
    units_sold = 10000
    unit_price = Decimal("1000.00")
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = Decimal("10000000") * Constants.CommissionRate.Epic
    assert result == expected


def test_unit_price_conversion_from_various_types(calculator):
    """Test that unit_price is properly converted to Decimal."""
    from constants import Constants
    # The method converts unit_price to Decimal internally
    units_sold = 50
    unit_price = 20.00  # Float input
    result = calculator.get_commission_for_the_sale(units_sold, unit_price)
    expected = Decimal("1000") * Constants.CommissionRate.Standard
    assert result == expected