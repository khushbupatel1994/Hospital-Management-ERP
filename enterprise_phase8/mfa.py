"""Optional TOTP MFA adapter. Install pyotp in production to enable it."""
try:
    import pyotp
except ImportError:
    pyotp = None

def available(): return pyotp is not None

def generate_secret():
    if not pyotp: raise RuntimeError("Install pyotp to enable TOTP MFA")
    return pyotp.random_base32()

def verify(secret: str, code: str) -> bool:
    if not pyotp: raise RuntimeError("Install pyotp to enable TOTP MFA")
    return bool(pyotp.TOTP(secret).verify(str(code), valid_window=1))
