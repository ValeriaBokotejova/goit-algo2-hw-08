"""
Throttling Rate Limiter for chat message frequency control.
"""

import time
import random
from typing import Dict

class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        # user_id -> timestamp of last message
        self.last_sent: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        """
        Return True if user can send a message now (enough time has passed).
        """
        now = time.time()
        last = self.last_sent.get(user_id)
        if last is None:
            return True
        return (now - last) >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        """
        Record a message send attempt.
        Returns True if allowed and records timestamp, False otherwise.
        """
        if self.can_send_message(user_id):
            self.last_sent[user_id] = time.time()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        If rate-limited, return seconds until next allowed message.
        If allowed now or user has no record, returns 0.0.
        """
        now = time.time()
        last = self.last_sent.get(user_id)
        if last is None:
            return 0.0
        wait = last + self.min_interval - now
        return max(wait, 0.0)

def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)
    print("\n=== Message flow simulation (Throttling) ===")
    for message_id in range(1, 11):
        user_id = str(message_id % 5 + 1)
        allowed = limiter.record_message(user_id)
        wait = limiter.time_until_next_allowed(user_id)
        status = "✓" if allowed else f"× (wait {wait:.1f}s)"
        print(f"Message {message_id:2d} | User {user_id} | {status}")
        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting 10 seconds...")
    time.sleep(10)

    print("\n=== New message series after wait ===")
    for message_id in range(11, 21):
        user_id = str(message_id % 5 + 1)
        allowed = limiter.record_message(user_id)
        wait = limiter.time_until_next_allowed(user_id)
        status = "✓" if allowed else f"× (wait {wait:.1f}s)"
        print(f"Message {message_id:2d} | User {user_id} | {status}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_throttling_limiter()
