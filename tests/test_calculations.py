import pytest
from app.calculations import add,BankAccount, InsufficientFunds

# Create pytest fixtures to store initializations that would otherwise be so repititive
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (7,1,8),
    (12,4,16)
])
def test_add(num1,num2,expected):
    print("Testing add function")
    assert expected==add(num1,num2)


@pytest.mark.parametrize("amount",[10,20,30,40,50,60,70,80,90])
def test_bank_set_initial_amount(amount):
    bank_account=BankAccount(amount)
    assert bank_account.balance==amount

def test_bank_initial_balance(zero_bank_account):
    assert 0==zero_bank_account.balance

@pytest.mark.parametrize("deposits",[10,20,30,40,50,60,70])
def test_bank_deposit_feature(deposits):
    bank_account=BankAccount(deposits)
    initial_balance=bank_account.balance
    bank_account.deposit(deposits)
    assert initial_balance+deposits==bank_account.balance

@pytest.mark.parametrize("deposited, withdrew, expected",[
    (200,100,100),
    (50,10,40)
])
def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance==expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)


