"""Phase 9 release verification helper."""
from pathlib import Path
import py_compile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
for p in ROOT.rglob("*.py"):
    if any(part in {"__pycache__", ".venv", "venv"} for part in p.parts):
        continue
    try:
        py_compile.compile(str(p), doraise=True)
    except Exception as exc:
        errors.append((p, str(exc)))
if errors:
    for p, e in errors:
        print(f"FAIL: {p}: {e}")
    raise SystemExit(1)
print("Python compilation: PASS")
print("Running pytest...")
result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT)
raise SystemExit(result.returncode)
