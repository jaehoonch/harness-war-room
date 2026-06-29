from loyalty_service import points_earned


def test_points_on_gross():
    assert points_earned(100.0, 0.10) == 100
