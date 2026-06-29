import shutil
from pathlib import Path

from supervisor import run_war_room

DEMO = Path(__file__).resolve().parents[2] / "demo_repo"

FIXED = "def apply_discount(price, pct):\n    return round(price * (1 - pct), 2)\n"


class FakeAgent:
    def __init__(self, role, out):
        self.role = role
        self.out = out

    def run(self, user):
        return self.out


def fake_agents():
    return {
        "triage": FakeAgent("triage", "order_service.py"),
        "repro": FakeAgent("repro", "covered by existing test"),
        "fix": FakeAgent("fix", FIXED),
        "review": FakeAgent("review", "PASS"),
    }


def test_loop_reaches_green(tmp_path):
    src = tmp_path / "repo"
    shutil.copytree(DEMO, src)
    events = list(run_war_room("discount is wrong", str(src), agents=fake_agents()))
    roles = [e["role"] for e in events]
    assert roles[:4] == ["triage", "repro", "fix", "review"]
    assert events[-1]["type"] == "finished"
    assert events[-1]["passed"] is True
