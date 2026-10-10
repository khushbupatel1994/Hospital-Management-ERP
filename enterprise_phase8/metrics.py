import time
class Metrics:
    def __init__(self): self.requests=0; self.errors=0; self.started=time.time()
    def request(self, ok=True):
        self.requests += 1
        if not ok: self.errors += 1
    def snapshot(self):
        return {"requests":self.requests,"errors":self.errors,"uptime_seconds":round(time.time()-self.started,2)}
METRICS=Metrics()
