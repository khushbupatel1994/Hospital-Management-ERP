"""Phase 7 centralized notifications and live operational events."""
from datetime import datetime, timezone
from threading import Lock

_lock = Lock()
_events = []
_seq = 0
MAX_EVENTS = 500

def publish(event_type, title, message, severity="info", data=None):
    global _seq
    with _lock:
        _seq += 1
        event = {
            "id": _seq,
            "type": event_type,
            "title": title,
            "message": message,
            "severity": severity,
            "data": data or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _events.append(event)
        if len(_events) > MAX_EVENTS:
            del _events[:-MAX_EVENTS]
        return event

def since(event_id=0, limit=50):
    with _lock:
        return [e for e in _events if e["id"] > event_id][-limit:]
