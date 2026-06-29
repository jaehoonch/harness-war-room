"""Recorded transcript for DEMO_MODE so the demo never depends on the network."""

REPLAY = [
    {"type": "step", "role": "triage", "content": "order_service.py: discount rounding"},
    {"type": "step", "role": "repro", "content": "failing: apply_discount(99.99,0.1)==89.99"},
    {"type": "step", "role": "fix", "content": "round(price*(1-pct), 2)"},
    {"type": "step", "role": "review", "content": "PASS", "passed": True},
    {"type": "finished", "role": "supervisor", "content": "done", "passed": True},
]
