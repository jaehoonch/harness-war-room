from agents import ROLES, make_agent


class FakeClient:
    def __init__(self):
        self.calls = []

    def complete(self, model, system, user):
        self.calls.append((model, system, user))
        return f"{model}:{user[:5]}"


def test_workers_use_mini_reviewer_uses_4o():
    assert make_agent("triage").model == "gpt-4o-mini"
    assert make_agent("repro").model == "gpt-4o-mini"
    assert make_agent("fix").model == "gpt-4o-mini"
    assert make_agent("review").model == "gpt-4o"


def test_all_roles_present():
    assert ROLES == ["triage", "repro", "fix", "review"]


def test_agent_runs_via_client():
    client = FakeClient()
    out = make_agent("fix", client=client).run("fix the bug")
    assert out.startswith("gpt-4o-mini:")
    assert client.calls[0][0] == "gpt-4o-mini"
