"""Demo order service that the War Room agents repair.

Contains a deliberate discount-rounding bug: prices are truncated to whole
units instead of rounded to cents.
"""
import math


def apply_discount(price: float, pct: float) -> float:
    return float(math.floor(price * (1 - pct)))  # bug: truncates cents
