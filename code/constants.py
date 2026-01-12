from decimal import Decimal


class Constants:
    class CommissionRate:
        Standard = Decimal("0.08")
        Earner = Decimal("0.11")
        Epic = Decimal("0.14")

    class CommissionThreshold:
        EpicSalesAmount = Decimal("15000")
        EpicUnitAmount = 600
        EarnerSalesAmount = Decimal("12000")
        EarnerUnitAmount = 400

    class Discount:
        PreferredCustomer = Decimal("0.2")
        BulkOrder = Decimal("0.5")

    class AccountThresholds:
        FreezeBalance = Decimal("900")
        CloseBalance = Decimal("100")