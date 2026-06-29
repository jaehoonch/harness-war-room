"""The four War Room agents and their model assignment."""

ROLES = ["triage", "repro", "fix", "review"]

_MODELS = {"triage": "gpt-4o-mini", "repro": "gpt-4o-mini", "fix": "gpt-4o-mini", "review": "gpt-4o"}
_PROMPTS = {
    "triage": "Classify the ask and name the file(s) to change.",
    "repro": "Write a failing pytest reproducing the bug.",
    "fix": "Produce the minimal patched source to make tests pass.",
    "review": "Verdict PASS/FAIL and any guardrail concerns on the diff.",
}


class Agent:
    def __init__(self, role, client=None):
        self.role = role
        self.model = _MODELS[role]
        self.system = _PROMPTS[role]
        self._client = client

    def run(self, user: str) -> str:
        client = self._client
        if client is None:
            from llm import default_client

            client = default_client()
        return client.complete(self.model, self.system, user)


def make_agent(role, client=None) -> Agent:
    if role not in ROLES:
        raise ValueError(f"unknown role: {role}")
    return Agent(role, client=client)
