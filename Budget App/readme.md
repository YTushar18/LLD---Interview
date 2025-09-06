Here’s the complete Low-Level Design (LLD) for a Budget Management System with support for:
	•	User creation
	•	Income & Expense tracking
	•	Wallet and balance management
	•	Pluggable funding strategies (Bank, Credit Card, etc.)

✅ SOLID Principles Used

Principle	Application
Single Responsibility	Each class has one responsibility (e.g., User, Wallet, Transaction, BudgetManager).
Open/Closed	FundingStrategy is open for extension (new funding sources), closed for modification.
Liskov Substitution	BankTransfer and CreditCard can be used wherever FundingStrategy is expected.
Interface Segregation	Interface (abstract base class) FundingStrategy is lean and task-focused.
Dependency Inversion	BudgetManager depends on abstraction FundingStrategy, not on concrete classes.


⸻

🧠 Design Patterns Used

Pattern	Where Used	Why
Strategy Pattern	FundingStrategy with BankTransfer, CreditCard	To allow different funding mechanisms without changing wallet logic.
Factory-like Encapsulation	BudgetManager.create_user()	Centralized user creation and management.
Composition over Inheritance	User has a Wallet, instead of inheriting	Follows Composition principle.
Encapsulation	Private data like user’s transactions managed only via Wallet	Protects internal state.
