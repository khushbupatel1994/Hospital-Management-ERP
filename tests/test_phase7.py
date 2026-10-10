from server.realtime import publish, since

def test_realtime_event_bus():
    e = publish("test", "Test", "hello")
    assert e["id"] > 0
    assert since(e["id"]-1, 10)[-1]["title"] == "Test"
