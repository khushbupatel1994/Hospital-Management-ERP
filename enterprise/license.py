"""Simple deployment license gate.

This is intentionally a local deployment control, not a cryptographic DRM system.
For a commercial rollout, replace the validator with a server-side signed license service.
"""
import json, os
from datetime import date
from config.paths import CONFIG_DIR

LICENSE_FILE = os.path.join(CONFIG_DIR, "license.json")

def status():
    if not os.path.exists(LICENSE_FILE):
        return {"licensed": False, "reason": "License file not installed"}
    try:
        data = json.load(open(LICENSE_FILE, encoding="utf-8"))
        expiry = data.get("expires")
        if expiry and date.fromisoformat(expiry) < date.today():
            return {"licensed": False, "reason": "License expired"}
        return {"licensed": bool(data.get("license_id")), "license_id": data.get("license_id", "")}
    except Exception:
        return {"licensed": False, "reason": "Invalid license file"}
