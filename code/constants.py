from decimal import Decimal
import json
import os


class Constants:
    class CommissionRate:
        _data_file = os.path.join(os.path.dirname(__file__), "commission_rates.json")
        
        @classmethod
        def _load_rates(cls):
            with open(cls._data_file, 'r') as f:
                rates = json.load(f)
            return {key: Decimal(value) for key, value in rates.items()}
        
        _rates = _load_rates.__func__(None)
        Standard = _rates["Standard"]
        Earner = _rates["Earner"]
        Epic = _rates["Epic"]

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