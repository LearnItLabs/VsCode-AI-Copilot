from decimal import Decimal
import math


class Financial:
    def get_rate_of_return(
        self, initial_cost: Decimal, sold_amount: Decimal, dividends_earned: Decimal
    ) -> Decimal:
        initial_cost = Decimal(initial_cost)
        sold_amount = Decimal(sold_amount)
        dividends_earned = Decimal(dividends_earned)
        return (sold_amount + dividends_earned - initial_cost) / initial_cost

    def get_annualized_rate_of_return(
        self,
        initial_cost: Decimal,
        sold_amount: Decimal,
        dividends_earned: Decimal,
        years_held: int,
    ) -> Decimal:
        # Preserve original C# formula using square root (.5 power),
        # even though comments note a different approach.
        initial_cost = Decimal(initial_cost)
        sold_amount = Decimal(sold_amount)
        dividends_earned = Decimal(dividends_earned)
        calculated_return = (sold_amount + dividends_earned) / initial_cost
        return Decimal(math.pow(float(calculated_return), 0.5)) - Decimal(1)

    def calculate_loan_payment(
        self, annual_interest_rate: Decimal, duration_in_months: int, loan_amount: Decimal
    ) -> Decimal:
        annual_interest_rate = Decimal(annual_interest_rate)
        loan_amount = Decimal(loan_amount)
        monthly_rate = annual_interest_rate / Decimal(12)
        denominator = (Decimal(1) + monthly_rate) ** int(duration_in_months) - Decimal(1)
        return (monthly_rate + (monthly_rate / denominator)) * loan_amount
