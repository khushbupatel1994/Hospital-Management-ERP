"""Secure client for the compiled hospital desktop application."""
import os, uuid, requests

class ERPApiClient:
    def __init__(self, base_url=None, api_key=None, timeout=90, verify=None):
        self.base_url = (base_url or os.getenv("ERP_API_URL", "")).rstrip("/")
        if not self.base_url: raise ValueError("ERP_API_URL must be configured")
        self.api_key = api_key or os.getenv("ERP_API_KEY", "")
        self.timeout = timeout
        self.verify = os.getenv("ERP_TLS_VERIFY", "true").lower() not in {"0", "false", "no"} if verify is None else verify
        self.token = None
    def _headers(self, auth=True):
        h = {"X-API-Key": self.api_key, "X-Request-ID": str(uuid.uuid4())}
        if auth and self.token: h["Authorization"] = f"Bearer {self.token}"
        return h
    def login(self, username, password):
        r = requests.post(self.base_url + "/api/v1/auth/login", json={"username": username, "password": password}, headers=self._headers(False), timeout=self.timeout, verify=self.verify); r.raise_for_status(); data=r.json(); self.token=data["access_token"]; return data
    def request(self, method, path, **kwargs):
        headers = self._headers(True)
        kwargs.setdefault("headers", headers)
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", self.verify)
        r = requests.request(method, self.base_url + path, **kwargs)
        r.raise_for_status()
        return r.json()

    def enterprise_dashboard(self):
        return self.request("GET", "/api/v1/dashboard/enterprise")

    def summary(self):
        r=requests.get(self.base_url+"/api/v1/summary",headers=self._headers(),timeout=self.timeout,verify=self.verify); r.raise_for_status(); return r.json()
    def ask_ai(self, question):
        r=requests.post(self.base_url+"/api/v1/ai/assistant",json={"question":question},headers=self._headers(),timeout=self.timeout,verify=self.verify); r.raise_for_status(); return r.json()

    def notifications(self, last_event_id=0, limit=50):
        return self.request("GET", "/api/v1/notifications", params={"last_event_id": last_event_id, "limit": limit})

    def notification_bootstrap(self):
        return self.request("GET", "/api/v1/notifications/bootstrap")

    def enterprise_health(self):
        return self.request("GET", "/api/v1/enterprise/health")

    def logout(self):
        try:
            return self.request("POST", "/api/v1/session/logout")
        finally:
            self.token = None
