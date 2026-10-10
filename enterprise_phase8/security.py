"""Production-oriented security primitives. Secrets must come from environment/secret manager."""
import hashlib, secrets, time
from datetime import datetime, timezone

class TokenRevocationStore:
    def __init__(self): self._revoked = {}
    def revoke(self, jti: str, exp: int): self._revoked[jti] = exp
    def is_revoked(self, jti: str) -> bool:
        now = int(time.time())
        self._revoked = {k:v for k,v in self._revoked.items() if v > now}
        return jti in self._revoked

REVOCATIONS = TokenRevocationStore()

def new_jti(): return secrets.token_urlsafe(24)

def password_fingerprint(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def utc_now(): return datetime.now(timezone.utc).isoformat()
