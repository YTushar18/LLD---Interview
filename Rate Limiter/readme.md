⸻

⏳ LLD Problem 4: Rate Limiter System

⸻

✅ Real-World Problem

You are building an API gateway or backend service and need to limit the number of requests:
	•	Per user
	•	Per IP
	•	Per API key

To prevent abuse, spamming, or DoS attacks, we use Rate Limiting.

⸻

🎯 Goals

*Requirement	Description*
Time-based window	Allow only N requests per X seconds
Per-user/IP/token	Different keys should be rate-limited separately
O(1) performance	Fast access for high-traffic APIs
Scalable & extensible	Plug in new strategies (e.g., Sliding Window, Token Bucket)


⸻

✅ Design Patterns & SOLID Principles

Concept	Usage
Strategy Pattern	To support multiple rate limiting algorithms
SRP	Each strategy has its own class
OCP	Easily extendable with new algorithms
DIP	RateLimiter uses interface, not a concrete strategy


⸻

📦 Supported Strategies

We’ll implement this one first:

✅ 1. Fixed Window Counter

“Allow max 5 requests per 10 seconds”

Example:
	•	Count requests per time window (e.g., 2025-09-03T12:00:00)
	•	Reset the counter every new window

Others (for later):
	•	Sliding Window
	•	Token Bucket
	•	Leaky Bucket

⸻

✅ Class Design Plan

+----------------------+
|   RateLimiter (API)  |◄───────── injects ───────┐
+----------------------+
| + allow_request(key) |
+----------------------+

+----------------------+
| RateLimitStrategy    |  <interface>
+----------------------+
| + allow(key): bool   |
+----------------------+

+-------------------------------+
| FixedWindowCounterStrategy    |
+-------------------------------+
| - window_size: int (seconds) |
| - max_requests: int          |
| - store: Dict[str, (count, start_time)] |
+-------------------------------+
| + allow(key): bool           |
+-------------------------------+

+-------------------------------+
| SlidingWindowLogStrategy    |
+-------------------------------+
| - window_size: int (seconds) |
| - max_requests: int          |
| - store: Dict[str, (count, start_time)] |
+-------------------------------+
| + allow(key): bool           |
+-------------------------------+

⸻

✅ Step-by-Step Implementation

1. Strategy Interface

from abc import ABC, abstractmethod

class RateLimitStrategy(ABC):
    @abstractmethod
    def allow(self, key: str) -> bool:
        pass


⸻

2. Fixed Window Counter Strategy

import time

class FixedWindowCounterStrategy(RateLimitStrategy):
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.request_store = {}  # key -> (count, start_time)

    def allow(self, key: str) -> bool:
        current_time = int(time.time())
        window_start = current_time - (current_time % self.window_size)

        count, last_window = self.request_store.get(key, (0, window_start))

        if last_window != window_start:
            # New window → reset counter
            self.request_store[key] = (1, window_start)
            return True

        if count < self.max_requests:
            self.request_store[key] = (count + 1, window_start)
            return True

        return False


⸻

3. RateLimiter Class (Main Entry)

class RateLimiter:
    def __init__(self, strategy: RateLimitStrategy):
        self.strategy = strategy

    def allow_request(self, key: str) -> bool:
        return self.strategy.allow(key)


⸻

🧪 Sample Usage

if __name__ == "__main__":
    # Allow 5 requests per 10 seconds
    strategy = FixedWindowCounterStrategy(window_size=10, max_requests=5)
    limiter = RateLimiter(strategy)

    user_key = "user_123"

    for i in range(10):
        allowed = limiter.allow_request(user_key)
        print(f"Request {i+1}: {'✅ Allowed' if allowed else '❌ Blocked'}")
        time.sleep(1)


⸻

✅ Output Example

Request 1: ✅ Allowed
Request 2: ✅ Allowed
Request 3: ✅ Allowed
Request 4: ✅ Allowed
Request 5: ✅ Allowed
Request 6: ❌ Blocked
Request 7: ❌ Blocked
Request 8: ❌ Blocked
Request 9: ❌ Blocked
Request 10: ❌ Blocked

(Then it resets after 10s)



⸻

✅ Summary

1. Feature	Design
2. Request tracking	Per key
3. Fixed window logic	Clean and efficient
4. Extensibility	Strategy Pattern
5. OOP Principles	SRP, OCP, DIP


