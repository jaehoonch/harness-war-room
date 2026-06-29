"""Tests for the production pipeline steps + adapters, fully mocked."""
import sys
from pathlib import Path

import pipeline
from runtime import RepoOps, Redeployer

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "demo_repo"))


class FakeAgent:
    def __init__(self, out):
        self.out = out

    def run(self, _):
        return self.out


class FakeProbe:
    def overcharge(self, ticket):
        return ticket["probe"], 89.99


TICKET = {"file": "order_service.py", "ask": "fix", "probe": "/price", "probe_field": "charged", "expected": 89.99}


def test_repro_detects_green_after_fix():
    ev = pipeline.repro(TICKET, FakeProbe())
    assert ev["role"] == "repro"
    assert ev["passed"] is True


def test_repro_flags_overcharge():
    class Bad:
        def overcharge(self, t):
            return t["probe"], 89.0
    assert pipeline.repro(TICKET, Bad())["passed"] is False


def test_redeploy_branches_and_triggers():
    calls = []
    ops = RepoOps("/tmp/repo", runner=lambda *a, **k: calls.append(a[0]))
    dep = Redeployer(runner=lambda *a, **k: calls.append(a[0]))
    ev = pipeline.redeploy(ops, dep, "Fix INC1")
    assert ev["role"] == "deploy"
    assert any("checkout" in c for c in calls)
    assert any("pipelines" in c for c in calls)
