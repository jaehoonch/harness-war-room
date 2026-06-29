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
        "short_description": "Customers overcharged — discount truncates cents",
        "description": "99.99 at 10% bills 89.00 instead of 89.99. Whole orders rounded down to dollars.",
        "file": "order_service.py",
        "ask": "Discount rounding is wrong: 99.99 at 10% should be 89.99, not 89.00.",
    },
    {
        "number": "INC0012346",
        "priority": "2 - High",
        "caller": "Finance",
        "short_description": "Sales tax off by a cent on invoices",
        "description": "Tax is floored, so a $19.99 item at 8.75% lands a penny under and invoices fail reconciliation.",
        "file": "tax_service.py",
        "ask": "Sales tax should round to cents: 19.99 at 0.0875 should be 21.74.",
    },
    {
        "number": "INC0012377",
        "priority": "3 - Moderate",
        "caller": "Loyalty Team",
        "short_description": "Points credited on net price, not gross",
        "description": "Refunds wipe loyalty points to zero instead of crediting back the unrefunded amount.",
        "file": "loyalty_service.py",
        "ask": "Loyalty points should be earned on gross price before discount, 1 point per dollar.",
    },
]

_BY_NUMBER = {t["number"]: t for t in TICKETS}


def get_ticket(number):
    return _BY_NUMBER.get(number)
