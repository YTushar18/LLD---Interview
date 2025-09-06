# Low Level Design for Budget Management System

from abc import ABC, abstractmethod
from typing import List, Dict
import uuid
import datetime

# =========================
# ENTITY CLASSES
# =========================

class User:
    """Represents a user in the system."""
    def __init__(self, name: str):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.wallet = Wallet()


class Wallet:
    """Represents a user's financial wallet, holds incomes and expenses."""
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: 'Transaction'):
        self.transactions.append(transaction)

    def get_balance(self):
        return sum(t.amount for t in self.transactions)


class Transaction:
    """Base class for a transaction (either income or expense)."""
    def __init__(self, amount: float, category: str, note: str = ''):
        self.id = str(uuid.uuid4())
        self.amount = amount  # income = +ve, expense = -ve
        self.category = category
        self.note = note
        self.timestamp = datetime.datetime.now()


# =========================
# STRATEGY PATTERN
# =========================

class FundingStrategy(ABC):
    """Abstract funding source strategy."""
    @abstractmethod
    def fund(self, wallet: Wallet, amount: float, category: str):
        pass


class BankTransfer(FundingStrategy):
    def fund(self, wallet: Wallet, amount: float, category: str):
        wallet.add_transaction(Transaction(amount, category, "Bank Transfer"))


class CreditCard(FundingStrategy):
    def fund(self, wallet: Wallet, amount: float, category: str):
        wallet.add_transaction(Transaction(amount, category, "Credit Card"))


# =========================
# BUDGET ENGINE
# =========================

class BudgetManager:
    """Manages user registration, income, expense, and budgeting."""
    def __init__(self):
        self.users: Dict[str, User] = {}

    def create_user(self, name: str) -> User:
        user = User(name)
        self.users[user.user_id] = user
        return user

    def add_income(self, user_id: str, amount: float, category: str, strategy: FundingStrategy):
        user = self.users.get(user_id)
        if user:
            strategy.fund(user.wallet, amount, category)

    def add_expense(self, user_id: str, amount: float, category: str, note: str = ''):
        user = self.users.get(user_id)
        if user:
            user.wallet.add_transaction(Transaction(-amount, category, note))

    def get_summary(self, user_id: str):
        user = self.users.get(user_id)
        if user:
            income = sum(t.amount for t in user.wallet.transactions if t.amount > 0)
            expense = sum(t.amount for t in user.wallet.transactions if t.amount < 0)
            return {
                'total_income': income,
                'total_expense': -expense,
                'balance': user.wallet.get_balance(),
                'transactions': [(t.amount, t.category, t.note) for t in user.wallet.transactions]
            }
        return None


# =========================
# DEMO USAGE
# =========================

if __name__ == "__main__":
    manager = BudgetManager()
    user = manager.create_user("Tushar")

    manager.add_income(user.user_id, 2000, "Salary", BankTransfer())
    manager.add_expense(user.user_id, 400, "Groceries", "Weekly groceries")
    manager.add_expense(user.user_id, 150, "Entertainment", "Movie night")

    summary = manager.get_summary(user.user_id)
    print(summary)
