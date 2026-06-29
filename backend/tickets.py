"""Mocked ServiceNow incident queue feeding the War Room.

No live ServiceNow connection — this is a static stand-in shaped like the
ServiceNow Table API (`/api/now/table/incident`) so the demo reads like a
real ITSM hand-off. Each incident maps to a file + the ask the agents work.
"""

TICKETS = [
    {
        "number": "INC0012345",
        "priority": "1 - Critical",
        "caller": "Billing Ops",
        "assignment_group": "Payments Engineering",
        "opened": "2026-06-29 08:14",
        "short_description": "Customers overcharged — discount truncates cents",
        "description": (
            "Multiple customers report final totals rounding to whole dollars. "
            "Example: a 99.99 item at 10% off bills 89.00 instead of 89.99. "
            "Spike started after the v3.2 pricing release. ~1,400 orders affected/day."
        ),
        "file": "order_service.py",
        "ask": "Discount rounding is wrong: 99.99 at 10% should be 89.99, not 89.00.",
        "probe": "/price?amount=99.99&pct=0.10",
        "probe_field": "charged",
        "expected": 89.99,
        "activity": [
            {"who": "Maria (L1 Support)", "at": "08:16", "note": "Caller confirms charged 89.00. Repro on 3 accounts. Bumping to P1."},
            {"who": "System", "at": "08:17", "note": "Linked CHG0008812 (pricing v3.2). Possible regression."},
            {"who": "Dev (L2)", "at": "08:31", "note": "Suspect apply_discount uses math.floor — truncates cents. Needs round to 2dp."},
        ],
    },
    {
        "number": "INC0012346",
        "priority": "2 - High",
        "caller": "Finance",
        "assignment_group": "Payments Engineering",
        "opened": "2026-06-29 09:02",
        "short_description": "Sales tax off by a cent on invoices",
        "description": (
            "Invoice reconciliation fails: $19.99 at 8.75% should total 21.74 but lands at 21.00. "
            "Tax is floored. Blocks month-end close for 2 regions."
        ),
        "file": "tax_service.py",
        "ask": "Sales tax should round to cents: 19.99 at 0.0875 should be 21.74.",
        "probe": "/tax?amount=19.99&rate=0.0875",
        "probe_field": "total",
        "expected": 21.74,
        "activity": [
            {"who": "Sam (Finance)", "at": "09:05", "note": "Pennies short across all invoices today. Audit flagged 312 docs."},
            {"who": "Dev (L2)", "at": "09:20", "note": "total_with_tax floors instead of rounding. Same pattern as INC0012345."},
        ],
    },
    {
        "number": "INC0012377",
        "priority": "3 - Moderate",
        "caller": "Loyalty Team",
        "assignment_group": "Payments Engineering",
        "opened": "2026-06-29 10:40",
        "short_description": "Loyalty points credited on net, not gross",
        "description": (
            "VIPs report fewer points than expected. Points are earned on discounted price; "
            "policy is 1 point per gross dollar before discount. 100 at 10% off should earn 100, earns 90."
        ),
        "file": "loyalty_service.py",
        "ask": "Loyalty points should be earned on gross price before discount, 1 point per dollar.",
        "probe": "/loyalty?gross=100&pct=0.10",
        "probe_field": "points",
        "expected": 100,
        "activity": [
            {"who": "Priya (Loyalty)", "at": "10:42", "note": "Member escalation: 90 pts instead of 100 on a $100 order."},
            {"who": "Dev (L2)", "at": "10:55", "note": "points_earned multiplies by (1-discount). Should use gross."},
        ],
    },
]

_BY_NUMBER = {t["number"]: t for t in TICKETS}


def get_ticket(number):
    return _BY_NUMBER.get(number)


_RCA = {
    "INC0012345": "Root cause: apply_discount() floors to whole dollars; cents are lost. Fix: round to 2 decimals. Verified 99.99@10% -> 89.99. Shipped in 2 review loops.",
    "INC0012346": "Root cause: total_with_tax() floors the taxed total. Fix: round to cents. 19.99@8.75% -> 21.74. Reconciliation restored.",
    "INC0012377": "Root cause: points earned on net (post-discount) price. Fix: credit on gross. 100@10% -> 100 points.",
}


def chat(number, question):
    t = get_ticket(number)
    if not t:
        return "Select a ticket first."
    rca = _RCA.get(number, "No RCA on file yet — dispatch the agents to generate one.")
    return f"{t['number']} · {t['short_description']}\nQ: {question}\nA: {rca}"

