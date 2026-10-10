"""Phase 6 client gateway for centralized ERP modules."""
from server.client import ERPApiClient

class RemoteGateway:
    def __init__(self, client=None):
        self.client = client or ERPApiClient()
    def modules(self):
        return self.client.request("GET", "/api/v1/modules")
    def list(self, module, limit=50, offset=0, search=""):
        return self.client.request("GET", f"/api/v1/modules/{module}/records", params={"limit":limit,"offset":offset,"search":search})
    def create(self, module, data):
        return self.client.request("POST", f"/api/v1/modules/{module}/records", json={"data":data})
    def update(self, module, record_id, data):
        return self.client.request("PUT", f"/api/v1/modules/{module}/records/{record_id}", json={"data":data})
    def delete(self, module, record_id):
        return self.client.request("DELETE", f"/api/v1/modules/{module}/records/{record_id}")
