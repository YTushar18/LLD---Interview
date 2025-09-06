from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
from abc import ABC, abstractmethod

# ===========================
# ENUMS & HELPERS
# ===========================
class RecurrenceType(Enum):
    NONE = "NONE"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


# ===========================
# MODELS: User, TimeSlot, Event
# ===========================
class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name


class TimeSlot:
    def __init__(self, start: datetime, end: datetime):
        assert end > start, "End time must be after start time"
        self.start = start
        self.end = end

    def overlaps(self, other: 'TimeSlot') -> bool:
        return self.start < other.end and other.start < self.end


class Event:
    def __init__(self, title: str, slot: TimeSlot, owner: User, recurrence: str = RecurrenceType.NONE):
        self.title = title
        self.slot = slot
        self.owner = owner
        self.recurrence = recurrence


# ===========================
# REPOSITORY INTERFACE (for storage abstraction)
# ===========================
class CalendarRepository(ABC):
    @abstractmethod
    def add_event(self, event: Event): pass

    @abstractmethod
    def get_events_for_user(self, user_id: str) -> List[Event]: pass


# ===========================
# IN-MEMORY REPOSITORY (simple TreeMap-like behavior)
# ===========================
class InMemoryCalendarRepository(CalendarRepository):
    def __init__(self):
        self.user_events = {}  # user_id -> List[Event]

    def add_event(self, event: Event):
        self.user_events.setdefault(event.owner.user_id, []).append(event)

    def get_events_for_user(self, user_id: str) -> List[Event]:
        return self.user_events.get(user_id, [])


# ===========================
# CALENDAR SERVICE
# ===========================
class CalendarService:
    def __init__(self, repository: CalendarRepository):
        self.repository = repository

    def is_conflicting(self, user: User, new_slot: TimeSlot) -> bool:
        events = self.repository.get_events_for_user(user.user_id)
        for event in events:
            if event.slot.overlaps(new_slot):
                return True
        return False

    def book_event(self, title: str, slot: TimeSlot, user: User, recurrence: str = RecurrenceType.NONE) -> Optional[str]:
        if self.is_conflicting(user, slot):
            return f"Conflict with another event for {user.name}"

        event = Event(title, slot, user, recurrence)
        self.repository.add_event(event)
        return None  # success


# ===========================
# DEMO / TESTING
# ===========================
if __name__ == "__main__":
    # Setup
    repo = InMemoryCalendarRepository()
    service = CalendarService(repo)

    # Users
    user1 = User("u1", "Tushar")

    # Booking 1
    now = datetime.now()
    slot1 = TimeSlot(now, now + timedelta(hours=2))
    conflict = service.book_event("Interview with PayPal", slot1, user1)
    print(conflict or "✅ Booked Interview")

    # Booking 2 - overlapping
    slot2 = TimeSlot(now + timedelta(hours=1), now + timedelta(hours=3))
    conflict = service.book_event("Meeting with Recruiter", slot2, user1)
    print(conflict or "✅ Booked Meeting")

    # Booking 3 - no overlap
    slot3 = TimeSlot(now + timedelta(hours=3), now + timedelta(hours=4))
    conflict = service.book_event("Deep Work", slot3, user1)
    print(conflict or "✅ Booked Deep Work")
