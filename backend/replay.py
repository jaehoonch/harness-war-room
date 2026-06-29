"""Recorded transcripts for DEMO_MODE so the demo never needs the network.

Keyed by ServiceNow incident. INC0012345 shows the harness loop earning its
keep: the first fix is rejected (tests still red), the agents retry, green.
"""

REPLAYS = {
    "INC0012345": [
        {"type": "step", "role": "triage", "content": "Mapped to order_service.py · apply_discount(); 1 test failing.", "file": "order_service.py"},
        {"type": "step", "role": "repro", "content": "test_discount_keeps_cents: apply_discount(99.99,0.10) -> 89.0, expected 89.99",
         "output": "FAILED test_order_service.py::test_discount_keeps_cents  89.0 != 89.99\n1 failed, 1 passed"},
        {"type": "step", "role": "fix", "content": "Attempt 1: drop math.floor", "loop": 1,
         "diff": "- return float(math.floor(price * (1 - pct)))\n+ return price * (1 - pct)"},
        {"type": "step", "role": "review", "content": "FAIL — float drift: 89.991 != 89.99. Round to cents.", "passed": False, "loop": 1,
         "output": "FAILED test_discount_keeps_cents  89.991 != 89.99\n1 failed, 1 passed"},
        {"type": "step", "role": "fix", "content": "Attempt 2: round to 2 decimals", "loop": 2,
         "diff": "- return float(math.floor(price * (1 - pct)))\n+ return round(price * (1 - pct), 2)"},
        {"type": "step", "role": "review", "content": "PASS — cents preserved, no guardrail concerns.", "passed": True, "loop": 2,
         "output": "2 passed in 0.04s"},
        {"type": "finished", "role": "supervisor", "content": "Shipped fix for INC0012345 in 2 loops.", "passed": True},
    ],
    "INC0012346": [
        {"type": "step", "role": "triage", "content": "Mapped to tax_service.py · total_with_tax(); 1 test failing.", "file": "tax_service.py"},
        {"type": "step", "role": "repro", "content": "total_with_tax(19.99,0.0875) -> 21.0, expected 21.74",
         "output": "FAILED test_tax_service.py::test_tax_rounds_to_cents  21.0 != 21.74\n1 failed"},
        {"type": "step", "role": "fix", "content": "round to cents", "loop": 1,
         "diff": "- return float(math.floor(price * (1 + rate)))\n+ return round(price * (1 + rate), 2)"},
        {"type": "step", "role": "review", "content": "PASS — invoice reconciles.", "passed": True, "loop": 1,
         "output": "1 passed in 0.03s"},
        {"type": "finished", "role": "supervisor", "content": "Shipped fix for INC0012346 in 1 loop.", "passed": True},
    ],
    "INC0012377": [
        {"type": "step", "role": "triage", "content": "Mapped to loyalty_service.py · points_earned(); 1 test failing.", "file": "loyalty_service.py"},
        {"type": "step", "role": "repro", "content": "points_earned(100,0.10) -> 90, expected 100",
         "output": "FAILED test_loyalty_service.py::test_points_on_gross  90 != 100\n1 failed"},
        {"type": "step", "role": "fix", "content": "earn on gross, not net", "loop": 1,
         "diff": "- net = gross * (1 - discount_pct)\n- return int(net)\n+ return int(gross)"},
        {"type": "step", "role": "review", "content": "PASS — points credited on gross.", "passed": True, "loop": 1,
         "output": "1 passed in 0.03s"},
        {"type": "finished", "role": "supervisor", "content": "Shipped fix for INC0012377 in 1 loop.", "passed": True},
    ],
}

DEFAULT = "INC0012345"
REPLAY = REPLAYS[DEFAULT]  # back-compat default transcript
