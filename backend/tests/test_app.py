import json

from agui import to_agui


def test_maps_to_agui_event_stream():
    internal = [
        {"type": "step", "role": "triage", "content": "order_service.py"},
        {"type": "finished", "role": "supervisor", "content": "done", "passed": True},
    ]
    events = list(to_agui(internal))
    assert events[0]["type"] == "RUN_STARTED"
    assert any(e["type"] == "STATE_DELTA" for e in events)
    assert events[-1]["type"] == "RUN_FINISHED"
    assert events[-1]["passed"] is True


def test_demo_mode_replays_to_green():
    import os

    os.environ["DEMO_MODE"] = "1"
    from fastapi.testclient import TestClient

    import app as appmod

    client = TestClient(appmod.app)
    r = client.get("/api/run", params={"ask": "discount wrong"})
    payload = [json.loads(l[6:]) for l in r.text.splitlines() if l.startswith("data: ")]
    assert payload[-1]["type"] == "RUN_FINISHED"
    assert payload[-1]["passed"] is True
