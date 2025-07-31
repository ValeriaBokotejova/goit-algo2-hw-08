# Flow Control & Rate Limiting Homework 🌊⏳
_repo: goit-algo2-hw-08_

Two implementations of a chat rate limiter to prevent spam.

---

## 1️⃣ Sliding Window Rate Limiter

**File:** `sliding_window_rate_limiter.py`

**Class:** `SlidingWindowRateLimiter(window_size=10, max_requests=1)`

**Methods:**

- `_cleanup_window(user_id, current_time)`
- `can_send_message(user_id)`
- `record_message(user_id)`
- `time_until_next_allowed(user_id)`

**Run:**

```bash
python sliding_window_rate_limiter.py
```

---

## 2️⃣ Throttling Rate Limiter

**File:** `throttling_rate_limiter.py`

**Class:** `ThrottlingRateLimiter(min_interval=10.0)`

**Methods:**

- `can_send_message(user_id)`
- `record_message(user_id)`
- `time_until_next_allowed(user_id)`

**Run:**

```bash
python throttling_rate_limiter.py
```
