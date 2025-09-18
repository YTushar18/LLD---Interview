from abc import ABC, abstractmethod
from enum import Enum
from typing import List
import threading
import time

# ---------- ENUMS ----------
class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Status(Enum):
    MOVING = 'Moving'
    IDLE = 'Idle'
    STOPPED = 'Stopped'

# ---------- REQUEST MODEL ----------
class Request:
    def __init__(self, source_floor: int, destination_floor: int):
        self.source_floor = source_floor
        self.destination_floor = destination_floor

# ---------- STRATEGY PATTERN: Scheduler Interface ----------
class SchedulingStrategy(ABC):
    @abstractmethod
    def select_elevator(self, elevators: List['Elevator'], request: Request) -> 'Elevator':
        pass

class NearestCarStrategy(SchedulingStrategy):
    def select_elevator(self, elevators: List['Elevator'], request: Request) -> 'Elevator':
        # Simple strategy: choose the closest idle elevator
        idle_elevators = [e for e in elevators if e.status == Status.IDLE]
        if idle_elevators:
            return min(idle_elevators, key=lambda e: abs(e.current_floor - request.source_floor))
        return min(elevators, key=lambda e: abs(e.current_floor - request.source_floor))

# ---------- ELEVATOR CLASS ----------
class Elevator:
    def __init__(self, id: int):
        self.id = id
        self.current_floor = 0
        self.status = Status.IDLE
        self.direction = Direction.IDLE
        self.request_queue: List[Request] = []
        self.lock = threading.Lock()

    def request(self, request: Request):
        with self.lock:
            print(f"[Elevator {self.id}] Request received: {request.source_floor} -> {request.destination_floor}")
            self.request_queue.append(request)
            if self.status == Status.IDLE:
                self.move()

    def move(self):
        def run():
            while self.request_queue:
                with self.lock:
                    req = self.request_queue.pop(0)
                    print(f"[Elevator {self.id}] Picking up from floor {req.source_floor}")
                    self.go_to_floor(req.source_floor)
                    print(f"[Elevator {self.id}] Dropping at floor {req.destination_floor}")
                    self.go_to_floor(req.destination_floor)
            self.status = Status.IDLE
            self.direction = Direction.IDLE
            print(f"[Elevator {self.id}] Now IDLE")
        threading.Thread(target=run).start()

    def go_to_floor(self, target_floor: int):
        self.status = Status.MOVING
        if target_floor > self.current_floor:
            self.direction = Direction.UP
        elif target_floor < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE
            print(f"[Elevator {self.id}] Already at floor {target_floor}")
            return
        while self.current_floor != target_floor:
            time.sleep(1)  # Simulate time to move
            self.current_floor += self.direction.value
            print(f"[Elevator {self.id}] Reached floor {self.current_floor}")
        self.status = Status.STOPPED
        print(f"[Elevator {self.id}] Doors opening at floor {self.current_floor}")
        time.sleep(1)
        print(f"[Elevator {self.id}] Doors closing")
        self.status = Status.MOVING

# ---------- ELEVATOR SYSTEM ----------
class ElevatorSystem:
    def __init__(self, num_elevators: int, strategy: SchedulingStrategy):
        self.elevators = [Elevator(i) for i in range(num_elevators)]
        self.strategy = strategy

    def pickup_request(self, request: Request):
        elevator = self.strategy.select_elevator(self.elevators, request)
        elevator.request(request)

# ---------- TEST ----------
if __name__ == "__main__":
    system = ElevatorSystem(num_elevators=2, strategy=NearestCarStrategy())

    # Simulate requests
    system.pickup_request(Request(2, 7))
    time.sleep(2)
    system.pickup_request(Request(3, 0))
    time.sleep(5)
    system.pickup_request(Request(5, 1))