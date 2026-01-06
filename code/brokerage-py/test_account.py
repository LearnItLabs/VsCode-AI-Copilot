import pytest

@pytest.fixture
def account():
    return {"balance": 100}

def test_initial_balance(account):
    assert account["balance"] == 100

def test_deposit(account):
    account["balance"] += 50
    assert account["balance"] == 150

def test_withdraw(account):
    account["balance"] -= 30
    assert account["balance"] == 70

def test_overdraw(account):
    account["balance"] = 50  # Set balance below withdrawal amount
    with pytest.raises(ValueError):
        if account["balance"] < 100:
            raise ValueError("Insufficient funds")