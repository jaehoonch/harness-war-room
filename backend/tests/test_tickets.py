import json

from fastapi.testclient import TestClient


def test_tickets_endpoint_lists_servicenow_incidents():
    import app as appmod

    client = TestClient(appmod.app)
    tk = client.get("/api/tickets").json()
    nums = [t["number"] for t in tk]
    assert "INC0012345" in nums
    assert all({"number", "priority", "file", "ask"} <= set(t) for t in tk)


def test_run_by_ticket_shows_red_then_green():
    import os

    os.environ["DEMO_MODE"] = "1"
    import app as appmod

    client = TestClient(appmod.app)
    r = client.get("/api/run", params={"ticket": "INC0012345"})
    ev = [json.loads(l[6:]) for l in r.text.splitlines() if l.startswith("data: ")]
    reviews = [e for e in ev if e.get("role") == "review" and "passed" in e]
    assert reviews[0]["passed"] is False  # first fix rejected
    assert ev[-1]["type"] == "RUN_FINISHED" and ev[-1]["passed"] is True
