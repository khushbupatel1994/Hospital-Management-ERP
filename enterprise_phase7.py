"""Phase 7 client-side integration helpers."""
from server.client import ERPApiClient
from server.remote_gateway import RemoteGateway
from server.live_client import LiveNotificationClient

class EnterpriseSession:
    def __init__(self, base_url=None, api_key=None):
        self.client = ERPApiClient(base_url=base_url, api_key=api_key)
        self.gateway = RemoteGateway(self.client)
        self.live = None

    def login(self, username, password):
        return self.client.login(username, password)

    def start_live_updates(self, on_event, interval=10):
        self.live = LiveNotificationClient(self.client, on_event, interval)
        self.live.start()

    def stop_live_updates(self):
        if self.live: self.live.stop()

    def logout(self):
        self.stop_live_updates()
        return self.client.logout()
