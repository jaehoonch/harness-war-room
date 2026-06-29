"""Demo tax service the War Room agents repair.

Bug: tax is truncated instead of rounded, so invoices land a cent short.
"""
import math


def total_with_tax(price: float, rate: float) -> float:
    return float(math.floor(price * (1 + rate)))  # bug: truncates cents
