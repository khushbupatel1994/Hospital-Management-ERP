import os, sys, urllib.request
base=os.getenv('ERP_API_BASE_URL','https://localhost')
paths=['/health','/api/v1/health']
for path in paths:
    try:
        req=urllib.request.Request(base.rstrip('/')+path, headers={'User-Agent':'ERP-Phase11-SmokeTest'})
        with urllib.request.urlopen(req, timeout=8) as r:
            print(path, r.status)
            if 200 <= r.status < 300: sys.exit(0)
    except Exception as e:
        print(path, 'not available:', e)
print('SMOKE TEST: FAIL')
sys.exit(1)
