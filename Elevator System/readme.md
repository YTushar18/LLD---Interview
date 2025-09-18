✅ Design Patterns Used

Pattern	Usage
Strategy Pattern	SchedulingStrategy interface and NearestCarStrategy allow plug-and-play scheduling logic.
Command Pattern	Each Request acts like a command with source and destination.
Singleton (optional)	Not implemented, but the system could have a singleton controller.
Observer (optional)	Can be used for notification system or UI updates.


⸻

✅ SOLID Principles Followed

Principle	How it’s Used
S - SRP	Each class has a single responsibility (Elevator, System, Strategy, Request).
O - OCP	New strategies can be added without changing core logic.
L - LSP	NearestCarStrategy can replace SchedulingStrategy without breaking functionality.
I - ISP	Not directly applicable here as no fat interface exists.
D - DIP	ElevatorSystem depends on the abstraction SchedulingStrategy.


⸻

✅ Key Components
	•	Request: Models a user request.
	•	Elevator: Handles request queue, direction, movement.
	•	SchedulingStrategy: Abstract strategy interface.
	•	NearestCarStrategy: Chooses the best elevator based on proximity.
	•	ElevatorSystem: Main orchestrator that dispatches requests.

⸻

Would you like me to add:
	•	Class diagram (UML)?
	•	Tests using pytest?
	•	Webhooks / notifications (Observer pattern)?
	•	Extend for multi-floor or admin panel?

Let me know your next learning target!