"""Background polling client for Phase 7 live hospital notifications."""
import threading, time

class LiveNotificationClient:
    def __init__(self, api_client, on_event=None, interval=10):
        self.api_client = api_client
        self.on_event = on_event or (lambda event: None)
        self.interval = max(2, interval)
        self.last_event_id = 0
        self._stop = threading.Event()
        self._thread = None

    def start(self):
        if self._thread and self._thread.is_alive(): return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="erp-live-notifications", daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def _run(self):
        while not self._stop.is_set():
            try:
                payload = self.api_client.notifications(self.last_event_id, 50)
                for event in payload.get("events", []):
                    self.last_event_id = max(self.last_event_id, int(event.get("id", 0)))
                    self.on_event(event)
            except Exception:
                pass
            self._stop.wait(self.interval)
