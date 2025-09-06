# Mini Venmo - Low Level Design in Python
# ----------------------------------------

# Supports: Users, Friend Requests, Account Balances, Peer-to-Peer Payments
# SOLID Principles and Patterns included

from typing import Dict, List, Optional
from abc import ABC, abstractmethod

# ----------------------------
# User and Account Management
# ----------------------------

class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.friends: List[int] = []  # Store user_ids of friends
        self.account = Account(self.user_id)

    def add_friend(self, other_user_id: int):
        if other_user_id not in self.friends:
            self.friends.append(other_user_id)

    def __repr__(self):
        return f"User({self.user_id}, {self.name}, Balance=${self.account.balance})"


# ---------------------
# Account for each user
# ---------------------

class Account:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.balance: float = 0.0

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount


# ------------------------
# Payment Strategy Pattern
# ------------------------

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, sender: User, receiver: User, amount: float):
        pass

class BalancePayment(PaymentStrategy):
    def pay(self, sender: User, receiver: User, amount: float):
        sender.account.withdraw(amount)
        receiver.account.deposit(amount)
        print(f"Transferred ${amount} from {sender.name} to {receiver.name}")


# --------------------
# Notification Pattern
# --------------------

class Notifier(ABC):
    @abstractmethod
    def notify(self, user: User, message: str):
        pass

class EmailNotifier(Notifier):
    def notify(self, user: User, message: str):
        print(f"[EMAIL] To: {user.name} | Message: {message}")


# --------------------
# Venmo System Manager
# --------------------

class MiniVenmo:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.payment_strategy: PaymentStrategy = BalancePayment()
        self.notifier: Notifier = EmailNotifier()

    def create_user(self, user_id: int, name: str):
        if user_id in self.users:
            raise Exception("User already exists")
        self.users[user_id] = User(user_id, name)
        print(f"User created: {name}")

    def add_friend(self, user_id: int, friend_id: int):
        user = self.get_user(user_id)
        friend = self.get_user(friend_id)
        user.add_friend(friend_id)
        friend.add_friend(user_id)
        self.notifier.notify(friend, f"{user.name} added you as a friend.")

    def deposit_money(self, user_id: int, amount: float):
        user = self.get_user(user_id)
        user.account.deposit(amount)
        print(f"{user.name} deposited ${amount}. New balance: ${user.account.balance}")

    def pay(self, sender_id: int, receiver_id: int, amount: float):
        sender = self.get_user(sender_id)
        receiver = self.get_user(receiver_id)
        if receiver_id not in sender.friends:
            raise Exception("Can only pay friends")
        self.payment_strategy.pay(sender, receiver, amount)
        self.notifier.notify(receiver, f"You received ${amount} from {sender.name}.")

    def get_user(self, user_id: int) -> User:
        if user_id not in self.users:
            raise Exception("User not found")
        return self.users[user_id]

    def print_users(self):
        for user in self.users.values():
            print(user)


# --------------------
# Example Usage
# --------------------
if __name__ == "__main__":
    venmo = MiniVenmo()
    venmo.create_user(1, "Alice")
    venmo.create_user(2, "Bob")

    venmo.add_friend(1, 2)
    venmo.deposit_money(1, 100)

    venmo.pay(1, 2, 30)

    venmo.print_users()
