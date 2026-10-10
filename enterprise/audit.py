import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timezone
from config.paths import APP_DATA_DIR

AUDIT_DIR = os.path.join(APP_DATA_DIR, "audit")
KEY_FILE = os.path.join(AUDIT_DIR, "audit.key")
LOG_FILE = os.path.join(AUDIT_DIR, "audit.jsonl")


def _key():
    os.makedirs(AUDIT_DIR, exist_ok=True)
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as f:
            f.write(secrets.token_bytes(32))
    with open(KEY_FILE, "rb") as f:
        return f.read()


def record(action, actor="system", role="system", success=True, metadata=None):
    """Append a privacy-minimal, hash-chained audit event."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": str(actor)[:80],
        "role": str(role)[:40],
        "action": str(action)[:120],
        "success": bool(success),
        "metadata": metadata or {},
    }
    previous = ""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "rb") as f:
                lines = f.readlines()
            if lines:
                previous = json.loads(lines[-1].decode("utf-8")).get("hash", "")
        except Exception:
            previous = ""
    payload = json.dumps({"previous": previous, "event": event}, sort_keys=True, separators=(",", ":")).encode()
    digest = hmac.new(_key(), payload, hashlib.sha256).hexdigest()
    event["previous_hash"] = previous
    event["hash"] = digest
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")


def verify_chain():
    if not os.path.exists(LOG_FILE):
        return True, 0
    previous = ""
    count = 0
    key = _key()
    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)
            saved = event.pop("hash", "")
            payload = json.dumps({"previous": previous, "event": event}, sort_keys=True, separators=(",", ":")).encode()
            expected = hmac.new(key, payload, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(saved, expected) or event.get("previous_hash", "") != previous:
                return False, count
            previous = saved
            count += 1
    return True, count
