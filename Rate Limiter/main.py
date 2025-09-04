from abc import ABC, abstractmethod
import time
from collections import deque
from flask import Flask, request, jsonify

# =====================================================
# STRATEGY INTERFACE (Abstract Base)
# =====================================================
# Design Pattern: Strategy Pattern
# Principle: Interface Segregation, Open/Closed
class RateLimitStrategy(ABC):
    @abstractmethod
    def allow(self, key: str) -> bool:
        pass


# =====================================================
# 1. FIXED WINDOW COUNTER STRATEGY
# =====================================================
# Allows N requests per time window of X seconds
class FixedWindowCounterStrategy(RateLimitStrategy):
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.store = {}  # key -> (count, window_start_time)

    def allow(self, key: str) -> bool:
        current_time = int(time.time())
        window_start = current_time - (current_time % self.window_size)

        count, last_window = self.store.get(key, (0, window_start))

        if last_window != window_start:
            # New window started
            self.store[key] = (1, window_start)
            return True

        if count < self.max_requests:
            self.store[key] = (count + 1, window_start)
            return True

        return False


# =====================================================
# 2. SLIDING WINDOW LOG STRATEGY
# =====================================================
# Tracks individual timestamps in a sliding window
class SlidingWindowLogStrategy(RateLimitStrategy):
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.logs = {}  # key -> deque of timestamps

    def allow(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window_size

        if key not in self.logs:
            self.logs[key] = deque()

        log = self.logs[key]
        while log and log[0] < window_start:
            log.popleft()

        if len(log) < self.max_requests:
            log.append(now)
            return True
        return False


# =====================================================
# 3. TOKEN BUCKET STRATEGY
# =====================================================
# Tokens refill over time. Requests consume tokens.
class TokenBucketStrategy(RateLimitStrategy):
    def __init__(self, refill_rate: float, capacity: int):
        self.refill_rate = refill_rate  # tokens per second
        self.capacity = capacity
        self.buckets = {}  # key -> (tokens, last_refill_time)

    def allow(self, key: str) -> bool:
        now = time.time()
        tokens, last_time = self.buckets.get(key, (self.capacity, now))

        # Add tokens based on time passed
        elapsed = now - last_time
        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)

        if tokens >= 1:
            self.buckets[key] = (tokens - 1, now)
            return True

        self.buckets[key] = (tokens, now)
        return False


# =====================================================
# MAIN RATE LIMITER CLASS (Uses Strategy)
# =====================================================
# Principle: Dependency Inversion, Open/Closed
class RateLimiter:
    def __init__(self, strategy: RateLimitStrategy):
        self.strategy = strategy

    def allow_request(self, key: str) -> bool:
        return self.strategy.allow(key)


# =====================================================
# FLASK APP + MIDDLEWARE INTEGRATION
# =====================================================
app = Flask(__name__)

# Choose one strategy to apply here:
# strategy = FixedWindowCounterStrategy(window_size=10, max_requests=5)
# strategy = SlidingWindowLogStrategy(window_size=10, max_requests=5)
strategy = TokenBucketStrategy(refill_rate=1, capacity=5)
rate_limiter = RateLimiter(strategy)


# Middleware to apply rate limiting
@app.before_request
def rate_limit_middleware():
    user_ip = request.remote_addr  # You can also use API key, token, etc.
    if not rate_limiter.allow_request(user_ip):
        return jsonify({"error": "Too many requests. Please wait."}), 429


@app.route("/api/data")
def protected_api():
    return jsonify({"message": "✅ You have accessed protected data."})


@app.route("/health")
def health_check():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
