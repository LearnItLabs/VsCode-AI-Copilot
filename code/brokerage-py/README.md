# Brokerage Python Port

A Python port of the C# `BrokerageLib` with equivalent functionality.

## Modules
- `constants.py`: Rates, thresholds, and discounts.
- `account.py`: `Account` with debit/credit and freeze logic.
- `commission_calculator.py`: Commission calculation by units and sales.
- `financial.py`: Rate of return, annualized return (as-is), and loan payment.
- `payment_date.py`: Future payment date with weekend adjustment.

## Quick Usage
```python
from decimal import Decimal
from datetime import datetime
from brokerage_py import Account, CommissionCalculator, Financial, PaymentDate, Constants

# Account
acct = Account("Alice", Decimal("1000"))
acct.debit(Decimal("150"))
acct.credit(Decimal("200"))
print(acct.balance, acct.account_frozen)

# Commission
calc = CommissionCalculator()
commission = calc.get_commission_for_the_sale(500, Decimal("25"))
print(commission)

# Financial
fin = Financial()
ror = fin.get_rate_of_return(Decimal("200"), Decimal("250"), Decimal("20"))
print(ror)

# Payment Date
pd = PaymentDate()
future = pd.calculate_future_payment_date(datetime(2026, 1, 2))
print(future)
```

## Notes
- Monetary values use `decimal.Decimal` to preserve precision.
- The annualized rate of return matches the original C# formula (square root), even though comments suggest a different approach.
- `PaymentDate` weekend handling mirrors the original, including the noted Sunday comment.