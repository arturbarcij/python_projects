"""
Python practice sheet 5. OOP principles.

Encapsulation: keep data on the object and change it only through methods.
Abstraction: a base class says what every subtype can do, not how.
Inheritance: a subtype reuses the base and adds its own rule.
Polymorphism: one call works on every subtype, and each subtype behaves its own way.

How to use:
  1. Replace each `pass` with your solution.
  2. Run:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice5.py
     One problem:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice5.py 1

Each problem prints PASS or FAIL.
"""
from abc import ABC
from multiprocessing import Value
import sys


# ---------------------------------------------------------------- 1
class Wallet:
    """Money stored internally. Outside code reads balance and cannot assign it.
    deposit and withdraw accept only a positive amount.
    withdraw that would make the balance negative raises ValueError."""

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance
        # hint: self.owner, self._balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount
        # hint: amount <= 0 raises ValueError

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount


# ---------------------------------------------------------------- 2
from abc import ABC, abstractmethod

class Account(ABC):
    """Base for every bank account. Implement owner, _balance, balance, deposit, withdraw
    with the same rules as Wallet.
    month_end is abstract: Account("Ana") must raise TypeError.
    Use ABC and abstractmethod."""
    
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance
    
    @property
    def balance(self) -> float:
        return self._balance
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
    
    @abstractmethod
    def month_end(self) -> None:
        pass
        # hint: from abc import ABC, abstractmethod. class Account(ABC), @abstractmethod


# ---------------------------------------------------------------- 3
class SavingsAccount(Account):
    """Reuses Account. month_end adds balance * rate / 12.
    rate defaults to 0.02."""

    def __init__(self, owner: str, balance: float = 0.0, rate: float = 0.02):
        super().__init__(owner, balance)
        self.rate = rate
        # hint: super().__init__(owner, balance), store rate on self

    def month_end(self) -> None:
        self._balance += self._balance * self.rate / 12


# ---------------------------------------------------------------- 4
class CheckingAccount(Account):
    """month_end subtracts a fee of 5."""

    def month_end(self) -> None:
        self._balance -= 5


# ---------------------------------------------------------------- 5
def apply_month_end(accounts: list) -> list:
    """Call month_end on every account. Return the balances in the same order."""
    balances = []
    for account in accounts:
        account.month_end()
        balances.append(account.balance)
    return balances
    # hint: one loop. The account decides what month_end means


# ---------------------------------------------------------------- 6
class BonusSavings(SavingsAccount):
    """month_end does the savings interest, then adds a flat bonus.
    bonus defaults to 0."""

    def __init__(self, owner: str, balance: float = 0.0, rate: float = 0.02, bonus: float = 0.0):
        super().__init__(owner, balance, rate)
        self.bonus = bonus
        # hint: super().__init__(owner, balance, rate)

    def month_end(self) -> None:
        super().month_end()
        self._balance += self.bonus
        # hint: super().month_end(), then add the bonus to the balance


# ================================================================ tests
def _check(name, got, expected):
    if got != expected:
        print(f"FAIL {name}\n      expected {expected!r}\n      got      {got!r}")
        return False
    return True


def _raises(name, fn, error):
    try:
        fn()
    except error:
        return True
    except Exception as e:
        print(f"FAIL {name}: raised {type(e).__name__}, expected {error.__name__}")
        return False
    print(f"FAIL {name}: expected {error.__name__}")
    return False


def _run_wallet():
    name = "Problem 1"
    wallet = Wallet("A", 50)
    if not _check(f"{name}: starting balance", wallet.balance, 50):
        return False
    wallet.deposit(25)
    if not _check(f"{name}: after deposit", wallet.balance, 75):
        return False
    wallet.withdraw(20)
    if not _check(f"{name}: after withdraw", wallet.balance, 55):
        return False
    if not _raises(f"{name}: deposit 0", lambda: wallet.deposit(0), ValueError):
        return False
    if not _raises(f"{name}: deposit -1", lambda: wallet.deposit(-1), ValueError):
        return False
    if not _raises(f"{name}: withdraw too much", lambda: wallet.withdraw(1000), ValueError):
        return False
    if not _raises(f"{name}: assign balance", lambda: setattr(wallet, "balance", 1), AttributeError):
        return False
    if not _check(f"{name}: balance unchanged", wallet.balance, 55):
        return False
    print(f"PASS {name}: Wallet")
    return True


def _run_account():
    name = "Problem 2"
    if not _raises(f"{name}: Account()", lambda: Account("Ana"), TypeError):
        return False
    print(f"PASS {name}: Account")
    return True


def _run_savings():
    name = "Problem 3"
    account = SavingsAccount("Ana", 120, 0.5)
    if not _check(f"{name}: isinstance", isinstance(account, Account), True):
        return False
    if not _raises(f"{name}: deposit 0", lambda: account.deposit(0), ValueError):
        return False
    account.month_end()
    if not _check(f"{name}: interest", account.balance, 125):
        return False
    print(f"PASS {name}: SavingsAccount")
    return True


def _run_checking():
    name = "Problem 4"
    account = CheckingAccount("Ben", 200)
    account.month_end()
    if not _check(f"{name}: fee", account.balance, 195):
        return False
    account.deposit(5)
    if not _check(f"{name}: deposit still works", account.balance, 200):
        return False
    print(f"PASS {name}: CheckingAccount")
    return True


def _run_apply():
    name = "Problem 5"
    accounts = [SavingsAccount("Ana", 120, 0.5), CheckingAccount("Ben", 200)]
    got = apply_month_end(accounts)
    if not _check(f"{name}: balances", got, [125, 195]):
        return False
    print(f"PASS {name}: apply_month_end")
    return True


def _run_bonus():
    name = "Problem 6"
    account = BonusSavings("Cara", 120, 0.5, 10)
    account.month_end()
    if not _check(f"{name}: interest plus bonus", account.balance, 135):
        return False
    if not _check(f"{name}: isinstance Savings", isinstance(account, SavingsAccount), True):
        return False
    if not _check(f"{name}: isinstance Account", isinstance(account, Account), True):
        return False
    print(f"PASS {name}: BonusSavings")
    return True


CUSTOM = {
    1: _run_wallet,
    2: _run_account,
    3: _run_savings,
    4: _run_checking,
    5: _run_apply,
    6: _run_bonus,
}


def run(num):
    name = f"Problem {num}"
    try:
        return CUSTOM[num]()
    except Exception as e:
        print(f"FAIL {name}: raised {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    which = [int(a) for a in sys.argv[1:]] or sorted(CUSTOM)
    results = [run(n) for n in which]
    print(f"\n{sum(results)}/{len(results)} passed")
