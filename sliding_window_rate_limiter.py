"""
Sliding Window Rate Limiter for chat message frequency control.
"""

import time
import random
from collections import deque
from typing import Dict

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        # user_id -> deque of timestamps
        self.history: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        """Remove timestamps older than the window for this user."""
        dq = self.history.get(user_id)
        if not dq:
            return
        cutoff = current_time - self.window_size
        while dq and dq[0] <= cutoff:
            dq.popleft()
        if not dq:
            del self.history[user_id]

    def can_send_message(self, user_id: str) -> bool:
        """Return True if user can send a message now."""
        now = time.time()
        self._cleanup_window(user_id, now)
        dq = self.history.get(user_id, deque())
        return len(dq) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        """
        Record a message send attempt.
        Returns True if message is allowed, False otherwise.
        """
        now = time.time()
        self._cleanup_window(user_id, now)
        if self.can_send_message(user_id):
            # Ensure deque exists
            dq = self.history.setdefault(user_id, deque())
            dq.append(now)
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        If user is rate-limited, return seconds until next allowed message.
        If allowed now, returns 0.0.
        """
        now = time.time()
        dq = self.history.get(user_id, deque())
        if len(dq) < self.max_requests:
            return 0.0
        # Oldest timestamp + window_size - now
        next_allowed = dq[0] + self.window_size - now
        return max(next_allowed, 0.0)

# Demonstration test
def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)
    print("\n=== Message flow simulation ===")
    for message_id in range(1, 11):
        user_id = str(message_id % 5 + 1)
        allowed = limiter.record_message(user_id)
        wait = limiter.time_until_next_allowed(user_id)
        status = "✓" if allowed else f"× (wait {wait:.1f}s)"
        print(f"Msg {message_id:2d} | User {user_id} | {status}")
        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting 4 seconds...")
    time.sleep(4)

    print("\n=== New message series after wait ===")
    for message_id in range(11, 21):
        user_id = str(message_id % 5 + 1)
        allowed = limiter.record_message(user_id)
        wait = limiter.time_until_next_allowed(user_id)
        status = "✓" if allowed else f"× (wait {wait:.1f}s)"
        print(f"Msg {message_id:2d} | User {user_id} | {status}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_rate_limiter()
