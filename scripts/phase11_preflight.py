import os, sys
from pathlib import Path

REQUIRED = ["DATABASE_URL", "JWT_SECRET"]
PROD_FLAGS = {"APP_ENV": "production", "TLS_REQUIRED": "true"}

def main():
    missing = [k for k in REQUIRED if not os.getenv(k)]
    wrong = [f"{k}={os.getenv(k)!r} (expected {v!r})" for k,v in PROD_FLAGS.items() if os.getenv(k) != v]
    if missing or wrong:
        print("PHASE11 PREFLIGHT: FAIL")
        if missing: print("Missing:", ", ".join(missing))
        if wrong:
            print("Invalid production settings:")
            for x in wrong: print(" -", x)
        return 1
    print("PHASE11 PREFLIGHT: PASS")
    return 0

if __name__ == '__main__': sys.exit(main())
