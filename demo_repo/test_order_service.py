from order_service import apply_discount


def test_discount_rounds_correctly():
    assert apply_discount(100.0, 0.15) == 85.0


def test_discount_keeps_cents():
    assert apply_discount(99.99, 0.10) == 89.99
