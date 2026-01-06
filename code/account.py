from decimal import Decimal

from constants import Constants


class Account:
    def __init__(self, customer_name: str, balance: Decimal):
        self._customer_name = customer_name
        self._balance = Decimal(balance)
        self._frozen = False

    @property
    def customer_name(self) -> str:
        return self._customer_name

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def account_frozen(self) -> bool:
        return self._frozen

    def debit(self, amount: Decimal) -> None:
        amount = Decimal(amount)
        if amount < 0:
            raise ValueError("amount")

        if amount > self._balance:
            # allow negative balances under some conditions
            # charge a service fee (not implemented in original C#)
            # freeze if below threshold
            if self._balance < Constants.AccountThresholds.FreezeBalance:
                self._frozen = True

        self._balance -= amount

    def credit(self, amount: Decimal) -> None:
        amount = Decimal(amount)
        if amount < 0:
            raise ValueError("amount")

        self._balance += amount
        if self._balance > 0:
            self._frozen = False
