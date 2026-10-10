import time

class SessionGuard:
    """Idle-session guard. UI may call touch() after user activity."""
    def __init__(self, timeout_minutes=30):
        self.timeout_seconds = max(1, int(timeout_minutes * 60))
        self.last_activity = time.monotonic()

    def touch(self):
        self.last_activity = time.monotonic()

    def expired(self):
        return (time.monotonic() - self.last_activity) >= self.timeout_seconds
