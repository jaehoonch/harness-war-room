import shutil
from pathlib import Path

from sandbox import run_tests

DEMO = Path(__file__).resolve().parents[2] / "demo_repo"


def test_buggy_repo_fails(tmp_path):
    src = tmp_path / "repo"
    shutil.copytree(DEMO, src)
    result = run_tests(str(src))
    assert result.passed is False
    assert "test_discount_keeps_cents" in result.output


def test_fixed_repo_passes(tmp_path):
    src = tmp_path / "repo"
    shutil.copytree(DEMO, src)
    (src / "order_service.py").write_text(
        "def apply_discount(price, pct):\n    return round(price * (1 - pct), 2)\n"
    )
    result = run_tests(str(src))
    assert result.passed is True
