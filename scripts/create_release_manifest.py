from pathlib import Path
import hashlib, json, zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'release-manifest.json'
EXCLUDE = {'.git', '__pycache__', '.pytest_cache', 'hospital.db'}

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(ROOT)
    if any(part in EXCLUDE for part in rel.parts): continue
    if rel.name == OUT.name: continue
    files.append({'path': str(rel).replace('\\','/'), 'sha256': sha256(p), 'size': p.stat().st_size})
OUT.write_text(json.dumps({'release':'Phase 11 RC','files':files}, indent=2), encoding='utf-8')
print(f'Wrote {OUT} ({len(files)} files)')
