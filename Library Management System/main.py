from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# ------------------------- BOOK ------------------------- #
class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True


# ------------------------- USER ------------------------- #
class User(ABC):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Member(User):
    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        self.borrowed_books = []

class Admin(User):
    def __init__(self, name: str, email: str):
        super().__init__(name, email)


# ------------------------- PENALTY STRATEGY ------------------------- #
class PenaltyCalculator(ABC):
    @abstractmethod
    def calculate_penalty(self, days_overdue: int) -> float:
        pass

class SimplePenalty(PenaltyCalculator):
    def calculate_penalty(self, days_overdue: int) -> float:
        return 2.0 * days_overdue  # $2 per day


# ------------------------- NOTIFIER ------------------------- #
class Notifier(ABC):
    @abstractmethod
    def send(self, user: User, message: str):
        pass

class EmailNotifier(Notifier):
    def send(self, user: User, message: str):
        print(f"[EMAIL] To: {user.email} | Message: {message}")


# ------------------------- TRANSACTION ------------------------- #
class Transaction:
    def __init__(self, user: User, book: Book, borrow_date: datetime):
        self.user = user
        self.book = book
        self.borrow_date = borrow_date
        self.due_date = borrow_date + timedelta(days=7)
        self.return_date = None

    def return_book(self):
        self.return_date = datetime.now()


# ------------------------- LIBRARY ------------------------- #
class Library:
    def __init__(self):
        self.catalog = {}  # isbn -> Book
        self.transactions = []
        self.penalty_calculator = SimplePenalty()
        self.notifier = EmailNotifier()

    def add_book(self, book: Book):
        self.catalog[book.isbn] = book

    def borrow_book(self, user: Member, isbn: str):
        book = self.catalog.get(isbn)
        if not book:
            return f"Book with ISBN {isbn} not found."

        if not book.is_available:
            return f"Book '{book.title}' is already borrowed."

        book.is_available = False
        user.borrowed_books.append(book)
        transaction = Transaction(user, book, datetime.now())
        self.transactions.append(transaction)
        self.notifier.send(user, f"You have borrowed '{book.title}' until {transaction.due_date.date()}.")
        return f"Book '{book.title}' borrowed successfully."

    def return_book(self, user: Member, isbn: str):
        book = self.catalog.get(isbn)
        if not book or book not in user.borrowed_books:
            return f"Invalid return request."

        transaction = next((t for t in self.transactions if t.book == book and t.user == user and t.return_date is None), None)
        if not transaction:
            return f"Transaction not found."

        transaction.return_book()
        book.is_available = True
        user.borrowed_books.remove(book)

        days_overdue = (transaction.return_date - transaction.due_date).days
        penalty = 0
        if days_overdue > 0:
            penalty = self.penalty_calculator.calculate_penalty(days_overdue)
            self.notifier.send(user, f"You returned '{book.title}' late. Penalty: ${penalty:.2f}")
        else:
            self.notifier.send(user, f"Thanks for returning '{book.title}' on time!")

        return f"Book '{book.title}' returned. Penalty: ${penalty:.2f}"

    def list_available_books(self):
        return [book.title for book in self.catalog.values() if book.is_available]