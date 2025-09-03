 class diagram for the full Parking Lot System we’ve just implemented, showing relationships, composition, and key attributes/methods.

⸻

🧱 Parking Lot System – Class Diagram

                           +------------------+
                           |   VehicleType    |◄────────────┐
                           +------------------+             │
                           |  + BIKE           |            │
                           |  + CAR            |            │
                           |  + TRUCK          |            │
                           +------------------+             │
                                                           │
                           +------------------+             │
                           |    SpotType      |◄────────┐   │
                           +------------------+         │   │
                           |  + BIKE           |        │   │
                           |  + COMPACT        |        │   │
                           |  + LARGE          |        │   │
                           +------------------+         │   │
                                                        │   │
┌───────────────────┐            ┌────────────────────┐ │   │
│     Vehicle        │──────────►│     ParkingSpot     │─┘   │
├───────────────────┤   1     1  ├────────────────────┤     │
│ - license_plate   │           │ - spot_id           │     │
│ - vehicle_type    │──────────►│ - spot_type         │     │
└───────────────────┘           │ - vehicle (nullable)│     │
                                └────────────────────┘     │

┌────────────────────┐         uses        ┌────────────────────┐
│      Ticket         │───────────────────►│    ParkingSpot      │
├────────────────────┤                    ├────────────────────┤
│ - ticket_id         │                    │ - spot_id           │
│ - vehicle           │                    │ - spot_type         │
│ - assigned_spot     │                    │ - vehicle           │
│ - entry_time        │                    └────────────────────┘
└────────────────────┘

┌────────────────────┐       1     *        ┌────────────────────┐
│   ParkingFloor      │◄────────────────────│    ParkingSpot      │
├────────────────────┤                      ├────────────────────┤
│ - floor_number      │                      │ - spot_id           │
│ - spots: List       │                      │ - spot_type         │
└────────────────────┘                      └────────────────────┘

┌────────────────────┐ uses    ┌────────────────────┐
│   ParkingLot        │────────►│ PricingStrategy     │
├────────────────────┤         ├────────────────────┤
│ - floors: List      │         │ - rates             │
│ - active_tickets    │         │ + calculate_price() │
└────────────────────┘         └────────────────────┘
      ▲       ▲
      │       │
  park/unpark │
      │       │
      ▼       ▼
┌──────────────────────────┐
│ park_vehicle(),          │
│ unpark_vehicle(),        │
│ get_available_spots()    │
└──────────────────────────┘


⸻

🧠 Notes

✅ Relationships
	•	Vehicle → VehicleType (Enum)
	•	ParkingSpot → SpotType (Enum)
	•	ParkingFloor is a collection of ParkingSpots
	•	ParkingLot contains multiple ParkingFloors
	•	Ticket ties a Vehicle to a ParkingSpot
	•	ParkingLot uses a Strategy Pattern via PricingStrategy

⸻

✅ OOP Principles Reflected
	•	Single Responsibility → Each class has one job
	•	Open/Closed → Easy to add new spot or vehicle types
	•	Dependency Inversion → ParkingLot depends on PricingStrategy abstraction

⸻

Absolutely! Here’s a clear and structured summary of all SOLID principles and design patterns used in your Parking Lot System LLD, along with exactly where and how they were applied.

⸻

✅ SOLID Principles

Principle	Description	How it’s Applied in Parking Lot LLD
S – Single Responsibility	Each class should have one and only one reason to change	- Vehicle: holds vehicle data only- ParkingSpot: handles spot assignment only- Ticket: just stores ticket info- PricingStrategy: pricing logic- ParkingLot: main controller
O – Open/Closed	Classes should be open for extension but closed for modification	- New SpotType, VehicleType enums can be added without changing core classes- PricingStrategy can be replaced or extended
L – Liskov Substitution	Subclasses should be substitutable for their base classes	- ParkingSpot, Vehicle, etc., could be extended (e.g., EVSpot, ElectricBike) without breaking existing logic
I – Interface Segregation	Clients should not be forced to depend on unused interfaces	- Each class has minimal methods; no unnecessary/bloated interfaces
D – Dependency Inversion	High-level modules should depend on abstractions, not concrete implementations	- ParkingLot depends on PricingStrategy, which can be swapped out (e.g., FlatRate, DynamicPricing)


⸻

✅ Design Patterns

Pattern	Type	Where & Why It’s Used
Enum	Creational	- VehicleType, SpotType: Enforces type safety and clean conditions
Strategy Pattern	Behavioral	- PricingStrategy: encapsulates pricing logic, easy to replace or extend
Composition	Structural	- ParkingLot ⟶ composed of ParkingFloors, which contain ParkingSpots
UUID / Factory ID	Utility	- Ticket uses uuid for unique ticket generation
Controller Pattern	Architectural	- ParkingLot acts as the main orchestrator, similar to a controller in MVC


⸻

🧠 Summary in Plain English
	•	Each class does one job (SRP).
	•	We’ve structured the system so that it’s easy to extend (new vehicle types, new pricing, new floors) without touching existing code (OCP).
	•	If tomorrow you want to introduce EV spots, QR payment, or multi-tier pricing, it fits right in.
	•	PricingStrategy is a perfect use of the Strategy pattern, showing how logic can be modular and swappable.
	•	The ParkingLot is cleanly separated from implementation details like how pricing is calculated (DIP).



------

If you want to implement multiple pricing strategies (e.g., FlatRate, Hourly, Weekend Discount, Dynamic Surge Pricing, etc.), you can elegantly do this using the Strategy Pattern in its full power.

⸻

✅ Why Use Multiple Pricing Strategies?

Different scenarios might demand different pricing logic:

Scenario	Strategy
Pay per hour	HourlyPricingStrategy
Fixed price for all vehicles	FlatRateStrategy
Weekend discount	WeekendDiscountStrategy
Surge during peak hours	SurgePricingStrategy
Custom logic per spot/zone	ZonalPricingStrategy


⸻

✅ Apply the Strategy Pattern Properly

We’ll:
	1.	Create an interface/base class PricingStrategy
	2.	Implement multiple concrete classes
	3.	Use dependency injection to plug the desired strategy into ParkingLot

⸻

🧱 Step-by-Step Implementation

1. 🧠 PricingStrategy Interface

from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, ticket) -> int:
        pass


⸻

2. 💵 FlatRateStrategy

class FlatRateStrategy(PricingStrategy):
    def __init__(self, flat_rate: int = 50):
        self.flat_rate = flat_rate

    def calculate_price(self, ticket):
        return self.flat_rate


⸻

3. ⏱ HourlyPricingStrategy (Already Used)

class HourlyPricingStrategy(PricingStrategy):
    def __init__(self):
        self.rates = {
            VehicleType.BIKE: 10,
            VehicleType.CAR: 20,
            VehicleType.TRUCK: 30
        }

    def calculate_price(self, ticket):
        from datetime import datetime
        hours = max(1, (datetime.now() - ticket.entry_time).seconds // 3600)
        return hours * self.rates[ticket.vehicle.vehicle_type]


⸻

4. 🎉 WeekendDiscountStrategy (Wraps Another Strategy)

import datetime

class WeekendDiscountStrategy(PricingStrategy):
    def __init__(self, base_strategy: PricingStrategy, discount_percent: float = 20.0):
        self.base_strategy = base_strategy
        self.discount_percent = discount_percent

    def calculate_price(self, ticket):
        base_price = self.base_strategy.calculate_price(ticket)
        if datetime.datetime.now().weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            return int(base_price * (1 - self.discount_percent / 100))
        return base_price


⸻

🧠 Step 5: Inject Strategy in ParkingLot

Update your ParkingLot constructor:

class ParkingLot:
    def __init__(self, floors: List[ParkingFloor], pricing_strategy: PricingStrategy):
        self.floors = floors
        self.active_tickets = {}
        self.pricing = pricing_strategy  # Strategy injected here


⸻

🧪 Step 6: Use It Dynamically

if __name__ == "__main__":
    from time import sleep

    # Spot setup
    spots = [
        ParkingSpot("B1", SpotType.BIKE),
        ParkingSpot("C1", SpotType.COMPACT),
        ParkingSpot("L1", SpotType.LARGE)
    ]
    floor = ParkingFloor(1, spots)

    # Choose pricing strategy dynamically
    base_strategy = HourlyPricingStrategy()
    weekend_strategy = WeekendDiscountStrategy(base_strategy)
    # flat_strategy = FlatRateStrategy(60)

    # Inject into ParkingLot
    parking_lot = ParkingLot([floor], pricing_strategy=weekend_strategy)

    ticket = parking_lot.park_vehicle("KA-01-HH1234", "CAR")
    sleep(1)
    if ticket:
        parking_lot.unpark_vehicle(ticket.ticket_id)


⸻

✅ Summary

Component	Role
PricingStrategy	Abstract base (Interface)
HourlyPricingStrategy	Default pricing by hour and vehicle
FlatRateStrategy	Fixed price per vehicle
WeekendDiscountStrategy	Wraps any other strategy and adds discounts
ParkingLot	Injects whichever strategy is required


⸻

✅ Benefits
	•	🔌 Easily swap pricing logic without touching ParkingLot
	•	💡 Combine strategies (like decorator pattern)
	•	📦 Clean separation of concerns (SRP + OCP + DIP)
	•	🤖 Ideal for A/B testing, config-driven pricing, dynamic behavior

⸻

