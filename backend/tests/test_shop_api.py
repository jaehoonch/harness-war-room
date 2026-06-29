"""shop-api exposes the live bug over HTTP and goes green when source is fixed."""
import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "demo_repo"))
spec = importlib.util.spec_from_file_location("shop_app", ROOT / "shop-api" / "app.py")
shop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shop)

client = TestClient(shop.app)


def test_health():
    assert client.get("/healthz").json() == {"ok": True}


def test_price_charged_present():
    r = client.get("/price", params={"amount": 99.99, "pct": 0.10}).json()
    assert "charged" in r


def test_tax_total_present():
    r = client.get("/tax", params={"amount": 19.99, "rate": 0.0875}).json()
    assert "total" in r


def test_loyalty_points_present():
    r = client.get("/loyalty", params={"gross": 100, "pct": 0.10}).json()
    assert "points" in r
