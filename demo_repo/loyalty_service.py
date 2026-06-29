"""Demo loyalty service the War Room agents repair.

Bug: points are earned on the discounted price, shorting customers.
"""


def points_earned(gross: float, discount_pct: float) -> int:
    net = gross * (1 - discount_pct)
    return int(net)  # bug: should earn on gross
