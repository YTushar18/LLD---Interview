from abc import ABC, abstractmethod
from typing import List, Dict

# ===========================
# ENUMS / CONSTANTS
# ===========================
# Enum-like class for discount types
class DiscountType:
    FLAT = "FLAT"
    PERCENTAGE = "PERCENTAGE"

# ===========================
# ITEM CLASS (Entity)
# ===========================
# SRP: Represents a product that can be purchased.
# Used in the CartItem class to associate quantity with an item.
class Item:
    def __init__(self, item_id: str, name: str, price: float):
        self.item_id = item_id
        self.name = name
        self.price = price


# ===========================
# INVENTORY + OBSERVER PATTERN
# ===========================

# Interface for Observer — used by classes like Cart to receive updates from Inventory
# Design Pattern: Observer
class StockObserver(ABC):
    @abstractmethod
    def notify(self, item_id: str, stock: int):
        pass

# Inventory manages stock levels for items
# - Follows SRP: Only handles stock logic.
# - Implements Observer pattern: Notifies subscribed observers (like Cart) when stock changes.
class Inventory:
    def __init__(self):
        self.stock: Dict[str, int] = {}
        self.observers: List[StockObserver] = []

    def set_stock(self, item_id: str, quantity: int):
        self.stock[item_id] = quantity
        self._notify_observers(item_id)

    def reduce_stock(self, item_id: str, quantity: int):
        if self.stock.get(item_id, 0) >= quantity:
            self.stock[item_id] -= quantity
            self._notify_observers(item_id)
            return True
        return False

    def get_stock(self, item_id: str) -> int:
        return self.stock.get(item_id, 0)

    def attach(self, observer: StockObserver):
        self.observers.append(observer)

    def _notify_observers(self, item_id):
        for obs in self.observers:
            obs.notify(item_id, self.stock.get(item_id, 0))


# ===========================
# CART & CART ITEM
# ===========================

# SRP: Wraps an Item and quantity into a single object used inside the Cart.
class CartItem:
    def __init__(self, item: Item, quantity: int):
        self.item = item
        self.quantity = quantity

# Cart holds items being purchased.
# - Implements StockObserver to get notified of stock changes.
# - Follows SRP: Only manages cart logic (add/remove).
# - OCP: Easy to extend behavior without modifying the Cart itself.
class Cart(StockObserver):
    def __init__(self, inventory: Inventory):
        self.items: Dict[str, CartItem] = {}
        self.inventory = inventory
        self.total_price = 0.0
        self.inventory.attach(self)  # Subscribe to inventory updates

    # Adds an item to cart if stock allows
    def add_item(self, item: Item, quantity: int):
        if self.inventory.reduce_stock(item.item_id, quantity):
            if item.item_id in self.items:
                self.items[item.item_id].quantity += quantity
            else:
                self.items[item.item_id] = CartItem(item, quantity)
        else:
            print(f"[OUT OF STOCK] {item.name}")

    # Removes item from cart and restores stock
    def remove_item(self, item_id: str):
        if item_id in self.items:
            removed = self.items.pop(item_id)
            self.inventory.set_stock(item_id, self.inventory.get_stock(item_id) + removed.quantity)

    # Inventory notifies when stock changes
    def notify(self, item_id: str, stock: int):
        print(f"[INVENTORY UPDATE] {item_id} → {stock} left")

    # Debugging method to print cart contents
    def list_cart(self):
        print("\n🛒 Cart Items:")
        for ci in self.items.values():
            print(f" - {ci.item.name} x {ci.quantity} @ ₹{ci.item.price:.2f}")


# ===========================
# DISCOUNT & PRICING ENGINE
# ===========================

# Value object to hold a discount type and value
class Discount:
    def __init__(self, discount_type: str, value: float):
        self.discount_type = discount_type
        self.value = value

# PricingEngine calculates total price of items
# - Follows SRP: Only calculates pricing.
# - Follows OCP: Can add new discount strategies without changing existing logic.
# - Strategy Pattern-like logic to switch between FLAT, PERCENTAGE, or MEGA SALE dynamically.
class PricingEngine:
    def __init__(self):
        self.discounts: Dict[str, Discount] = {}
        self.mega_sale_active = False

    # Assign a discount to a specific item
    def apply_discount(self, item_id: str, discount: Discount):
        self.discounts[item_id] = discount

    # Turn on/off global mega sale
    def toggle_mega_sale(self, status: bool):
        self.mega_sale_active = status

    # Compute total cart price, applying discounts where relevant
    def calculate_total(self, cart: Cart) -> float:
        total = 0.0
        for ci in cart.items.values():
            price = ci.item.price
            if self.mega_sale_active:
                price *= 0.5  # 50% off
            elif ci.item.item_id in self.discounts:
                d = self.discounts[ci.item.item_id]
                if d.discount_type == DiscountType.FLAT:
                    price -= d.value
                elif d.discount_type == DiscountType.PERCENTAGE:
                    price *= (1 - d.value / 100)
            total += price * ci.quantity
        return round(total, 2)


# ===========================
# DEMO SIMULATION
# ===========================
if __name__ == "__main__":
    # Setup: inventory, pricing, and cart
    inventory = Inventory()
    pricing = PricingEngine()
    cart = Cart(inventory)

    # Item catalog
    iphone = Item("I001", "iPhone 15", 79990)
    mouse = Item("M001", "Logitech Mouse", 1299)
    book = Item("B001", "Atomic Habits", 499)

    # Set stock levels
    inventory.set_stock("I001", 5)
    inventory.set_stock("M001", 10)
    inventory.set_stock("B001", 20)

    # Cart operations
    cart.add_item(iphone, 1)
    cart.add_item(mouse, 2)
    cart.add_item(book, 1)

    # View cart
    cart.list_cart()

    # Apply item-specific discounts
    pricing.apply_discount("M001", Discount(DiscountType.PERCENTAGE, 20))
    pricing.apply_discount("B001", Discount(DiscountType.FLAT, 100))

    # Price before mega sale
    print("\n💰 Total before Mega Sale:", pricing.calculate_total(cart))

    # Enable mega sale
    pricing.toggle_mega_sale(True)
    print("💥 Mega Sale ON!")
    print("💰 Total during Mega Sale:", pricing.calculate_total(cart))