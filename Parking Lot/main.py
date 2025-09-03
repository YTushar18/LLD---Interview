from enum import Enum
from datetime import datetime
import uuid
from typing import List


# =====================================================
# ENUMS
# =====================================================

# VehicleType Enum - ensures type safety and clarity
class VehicleType(Enum):
    BIKE = "BIKE"
    CAR = "CAR"
    TRUCK = "TRUCK"

# SpotType Enum - defines parking spot categories
class SpotType(Enum):
    BIKE = "BIKE"
    COMPACT = "COMPACT"
    LARGE = "LARGE"


# =====================================================
# VEHICLE CLASS
# =====================================================

# Represents a Vehicle entering the lot
# ✅ S (Single Responsibility) - only holds vehicle data
class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type


# =====================================================
# PARKING SPOT CLASS
# =====================================================

# A parking spot holds one vehicle and tracks its type
# ✅ O (Open/Closed): New spot types can be added easily
class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType):
        self.spot_id = spot_id
        self.spot_type = spot_type 
        self.vehicle = None  # Holds assigned vehicle

    def is_available(self):
        return self.vehicle is None

    def assign_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def remove_vehicle(self):
        self.vehicle = None


# =====================================================
# TICKET CLASS
# =====================================================

# Ticket is created on entry and closed on exit
# ✅ S (Single Responsibility): Just holds ticket metadata
class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.assigned_spot = spot
        self.entry_time = datetime.now()


# =====================================================
# STRATEGY PATTERN → PRICING STRATEGY
# =====================================================

# Encapsulates pricing logic; easy to swap or modify
# ✅ Strategy Pattern
# ✅ O (Open/Closed): Can add dynamic/hourly pricing strategies
class PricingStrategy:
    def __init__(self):
        # Price per hour by vehicle type
        self.rates = {
            VehicleType.BIKE: 10,
            VehicleType.CAR: 20,
            VehicleType.TRUCK: 30
        }

    def calculate_price(self, ticket: Ticket) -> int:
        exit_time = datetime.now()
        hours = max(1, (exit_time - ticket.entry_time).seconds // 3600)
        return hours * self.rates[ticket.vehicle.vehicle_type]


# =====================================================
# PARKING FLOOR CLASS
# =====================================================

# Floor contains multiple parking spots and provides lookup
# ✅ S, O, L - Clear logic, can be extended to EV, handicapped spots
class ParkingFloor:
    def __init__(self, floor_number: int, spots: List[ParkingSpot]):
        self.floor_number = floor_number
        self.spots = spots

    # Find a compatible spot for the vehicle
    def get_available_spot(self, vehicle_type: VehicleType):
        for spot in self.spots:
            if spot.is_available() and self._can_fit(vehicle_type, spot.spot_type):
                return spot
        return None

    # Compatibility logic between vehicle and spot
    def _can_fit(self, v_type, s_type):
        if v_type == VehicleType.BIKE and s_type == SpotType.BIKE:
            return True
        if v_type == VehicleType.CAR and s_type in [SpotType.COMPACT, SpotType.LARGE]:
            return True
        if v_type == VehicleType.TRUCK and s_type == SpotType.LARGE:
            return True
        return False

    # Spot count per type on this floor
    def get_available_counts(self):
        counts = {
            SpotType.BIKE: 0,
            SpotType.COMPACT: 0,
            SpotType.LARGE: 0
        }
        for spot in self.spots:
            if spot.is_available():
                counts[spot.spot_type] += 1
        return counts


# =====================================================
# PARKING LOT MAIN CLASS (Controller)
# =====================================================

# ParkingLot is the orchestrator (composition of floors)
# ✅ S: Core coordinator
# ✅ D: Uses abstractions (Vehicle, Ticket, PricingStrategy)
class ParkingLot:
    def __init__(self, floors: List[ParkingFloor]):
        self.floors = floors
        self.active_tickets = {}  # ticket_id -> Ticket
        self.pricing = PricingStrategy()  # Strategy Pattern

    # Park vehicle → Find spot → Assign ticket
    def park_vehicle(self, license_plate: str, vehicle_type: str):
        vehicle = Vehicle(license_plate, VehicleType(vehicle_type))

        for floor in self.floors:
            spot = floor.get_available_spot(vehicle.vehicle_type)
            if spot:
                spot.assign_vehicle(vehicle)
                ticket = Ticket(vehicle, spot)
                self.active_tickets[ticket.ticket_id] = ticket
                print(f"[PARKED] Vehicle {license_plate} at spot {spot.spot_id} (Floor {floor.floor_number})")
                print(f"         Ticket ID: {ticket.ticket_id}\n")
                return ticket

        print(f"[FULL] No available spots for {vehicle_type}\n")
        return None

    # Unpark → calculate price → release spot
    def unpark_vehicle(self, ticket_id: str):
        ticket = self.active_tickets.get(ticket_id)
        if not ticket:
            print("[ERROR] Invalid ticket ID\n")
            return

        spot = ticket.assigned_spot
        spot.remove_vehicle()
        price = self.pricing.calculate_price(ticket)
        print(f"[UNPARKED] Vehicle {ticket.vehicle.license_plate} from spot {spot.spot_id}")
        print(f"           Charge: ₹{price}\n")
        del self.active_tickets[ticket_id]

    # Aggregate available spots per floor
    def get_available_spots(self):
        result = {}
        for floor in self.floors:
            floor_counts = floor.get_available_counts()
            result[f"Floor {floor.floor_number}"] = floor_counts
        return result


# =====================================================
# DEMO SIMULATION
# =====================================================

if __name__ == "__main__":
    from time import sleep

    # Create spots for floor 1
    spots = [
        ParkingSpot("B1", SpotType.BIKE),
        ParkingSpot("B2", SpotType.BIKE),
        ParkingSpot("C1", SpotType.COMPACT),
        ParkingSpot("C2", SpotType.COMPACT),
        ParkingSpot("L1", SpotType.LARGE),
        ParkingSpot("L2", SpotType.LARGE)
    ]

    # Setup parking system with 2 floor
    floor1 = ParkingFloor(1, spots) # - floor 1
    floor2 = ParkingFloor(2, spots) # - floor 2
    parking_lot = ParkingLot([floor1, floor2])

    print("\n--- [INITIAL SPOT COUNTS] ---")
    print(parking_lot.get_available_spots())

    # Park 3 vehicles
    t1 = parking_lot.park_vehicle("KA-01-AA1234", "CAR")
    t2 = parking_lot.park_vehicle("KA-02-BB5678", "BIKE")
    t3 = parking_lot.park_vehicle("KA-03-CC9999", "TRUCK")

    print("\n--- [SPOTS AFTER PARKING] ---")
    print(parking_lot.get_available_spots())

    sleep(1)  # Simulate 1 hour

    # Unpark car
    if t1:
        parking_lot.unpark_vehicle(t1.ticket_id)

    print("\n--- [SPOTS AFTER UNPARKING CAR] ---")
    print(parking_lot.get_available_spots())