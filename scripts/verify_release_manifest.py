from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'release-manifest.json'

def sha256(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024), b''): h.update(c)
 return h.hexdigest()

def main():
 if not M.exists(): print('MANIFEST: MISSING'); return 1
 data=json.loads(M.read_text(encoding='utf-8'))
 bad=[]
 for item in data['files']:
  p=ROOT/item['path']
  if not p.exists(): bad.append((item['path'],'missing')); continue
  if sha256(p)!=item['sha256']: bad.append((item['path'],'hash mismatch'))
 if bad:
  print('MANIFEST: FAIL')
  for x in bad: print(' -',x[0],x[1])
  return 1
 print(f"MANIFEST: PASS ({len(data['files'])} files verified)")
 return 0
if __name__=='__main__': sys.exit(main())
