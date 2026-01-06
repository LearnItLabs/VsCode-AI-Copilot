from decimal import Decimal

from constants import Constants


class CommissionCalculator:
    def get_commission_for_the_sale(self, units_sold: int, unit_price: Decimal) -> Decimal:
        if units_sold < 0:
            raise ValueError("UnitsSold cannot be less than zero.")

        unit_price = Decimal(unit_price)
        if unit_price < 0:
            raise ValueError("unitPrice cannot be less than zero.")

        gross_sale = Decimal(units_sold) * unit_price

        if (
            gross_sale >= Constants.CommissionThreshold.EpicSalesAmount
            or units_sold >= Constants.CommissionThreshold.EpicUnitAmount
        ):
            return gross_sale * Constants.CommissionRate.Epic
        elif (
            gross_sale >= Constants.CommissionThreshold.EarnerSalesAmount
            or units_sold >= Constants.CommissionThreshold.EarnerUnitAmount
        ):
            return gross_sale * Constants.CommissionRate.Earner
        else:
            return gross_sale * Constants.CommissionRate.Standard
