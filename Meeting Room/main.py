from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict

# ============================
# DOMAIN CLASSES
# ============================
class TimeSlot:
    def __init__(self, start: datetime, end: datetime):
        if start >= end:
            raise ValueError("Start time must be before end time")
        self.start = start
        self.end = end

    def overlaps(self, other: 'TimeSlot') -> bool:
        return not (self.end <= other.start or other.end <= self.start)

    def __repr__(self):
        return f"[{self.start} to {self.end}]"


class User:
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email


class Meeting:
    def __init__(self, meeting_id: str, title: str, timeslot: TimeSlot, organizer: User, attendees: List[User]):
        self.meeting_id = meeting_id
        self.title = title
        self.timeslot = timeslot
        self.organizer = organizer
        self.attendees = attendees


class MeetingRoom:
    def __init__(self, room_id: str, name: str):
        self.room_id = room_id
        self.name = name
        self.bookings: List[Meeting] = []

    def is_available(self, timeslot: TimeSlot) -> bool:
        return all(not m.timeslot.overlaps(timeslot) for m in self.bookings)

    def book_meeting(self, meeting: Meeting):
        if not self.is_available(meeting.timeslot):
            raise Exception(f"Room '{self.name}' is not available during {meeting.timeslot}")
        self.bookings.append(meeting)


# ============================
# NOTIFICATION STRATEGY (STRATEGY PATTERN)
# ============================
class NotificationSender(ABC):
    @abstractmethod
    def send(self, user: User, meeting: Meeting):
        pass


class EmailNotification(NotificationSender):
    def send(self, user: User, meeting: Meeting):
        print(f"[Email] To: {user.email}, Subject: Meeting '{meeting.title}' at {meeting.timeslot}")


# ============================
# CALENDAR SERVICE (SRP, OCP)
# ============================
class CalendarService:
    def __init__(self, rooms: List[MeetingRoom], notification_sender: NotificationSender):
        self.rooms = {room.room_id: room for room in rooms}
        self.notification_sender = notification_sender

    def book_room(self, room_id: str, meeting: Meeting):
        room = self.rooms.get(room_id)
        if not room:
            raise Exception("Meeting room not found")

        room.book_meeting(meeting)
        print(f"✅ Meeting '{meeting.title}' booked in room '{room.name}' at {meeting.timeslot}")

        # Notify attendees
        for attendee in meeting.attendees:
            self.notification_sender.send(attendee, meeting)


# ============================
# DEMO
# ============================
if __name__ == "__main__":
    room1 = MeetingRoom("R1", "Ocean View")
    room2 = MeetingRoom("R2", "Sky Lounge")

    user1 = User("U1", "alice@example.com")
    user2 = User("U2", "bob@example.com")

    slot1 = TimeSlot(datetime(2025, 9, 4, 10, 0), datetime(2025, 9, 4, 11, 0))
    slot2 = TimeSlot(datetime(2025, 9, 4, 10, 30), datetime(2025, 9, 4, 12, 0))

    meeting1 = Meeting("M1", "Team Sync", slot1, user1, [user1, user2])
    meeting2 = Meeting("M2", "Project Review", slot2, user2, [user2])

    service = CalendarService([room1, room2], EmailNotification())

    service.book_room("R1", meeting1)
    try:
        service.book_room("R1", meeting2)  # This will raise conflict error
    except Exception as e:
        print(f"❌ {e}")

    service.book_room("R2", meeting2)  # This should succeed
