"""shop-api: the live "problematic application" the War Room agents repair.

Imports the same demo_repo services, so any defect on disk is observable over
HTTP. Repro = a real call that overcharges; redeploy after a fix flips it green.
"""
import sys
from pathlib import Path

from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "demo_repo"))

from loyalty_service import points_earned  # noqa: E402
from order_service import apply_discount  # noqa: E402
from tax_service import total_with_tax  # noqa: E402

app = FastAPI(title="shop-api")


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/price")
def price(amount: float, pct: float = 0.0):
    return {"amount": amount, "pct": pct, "charged": apply_discount(amount, pct)}


@app.get("/tax")
def tax(amount: float, rate: float = 0.0):
    return {"amount": amount, "rate": rate, "total": total_with_tax(amount, rate)}


@app.get("/loyalty")
def loyalty(gross: float, pct: float = 0.0):
    return {"gross": gross, "pct": pct, "points": points_earned(gross, pct)}
