✅ SOLID Principles

1. S — Single Responsibility Principle

Each class has one clear job:

Class	Responsibility
User	Represents a user with name and email
TimeSlot	Encapsulates start and end datetime, handles overlap checking
MeetingRoom	Holds room name and manages its list of bookings
Meeting	Represents a meeting with title, host, attendees, and time
BookingService	Coordinates the logic for booking a meeting room
NotificationSender	Abstract base class for all notification methods
EmailNotificationSender	Handles sending emails only


⸻

2. O — Open/Closed Principle

Classes are open for extension but closed for modification:
	•	You can add new types of notifications (e.g., SlackNotificationSender, SMSNotificationSender) without changing the base NotificationSender logic.
	•	Booking conflict resolution is encapsulated and can be extended if we move to a different overlap check or conflict policy.

⸻

3. L — Liskov Substitution Principle
	•	EmailNotificationSender inherits from NotificationSender and can be substituted anywhere the base class is expected.
	•	Future subclasses (like SlackNotificationSender) will also obey this.

⸻

4. I — Interface Segregation Principle
	•	The NotificationSender interface is focused. It doesn’t force unrelated methods like logging or scheduling. Just one job: send.

⸻

5. D — Dependency Inversion Principle
	•	High-level module BookingService depends on the NotificationSender abstraction, not on any concrete class.
	•	This allows injection of different senders (email, SMS, etc.) easily.

⸻

✅ Design Patterns

Pattern	Usage
Strategy Pattern	Used to inject different notification strategies via NotificationSender (Email, Slack, etc.)
Factory-Like Initialization (Optional)	BookingService can be further abstracted with a factory for creating meetings/bookings.
Fail-Fast	Immediate exceptions thrown when a room is unavailable – fast feedback loop.
Encapsulation	TimeSlot encapsulates overlap logic, not exposed to other classes directly.


⸻

✅ Core Components and Responsibilities

Component	Role
User	Represents a person in the meeting
TimeSlot	Start/End datetime, overlap detection logic
MeetingRoom	Manages existing meetings for a room, validates conflicts
Meeting	Encapsulates all metadata for a meeting instance
NotificationSender	Base strategy for notifications
EmailNotificationSender	Implements actual email sending (simulated)
BookingService	High-level controller to handle room booking and attendee notifications


