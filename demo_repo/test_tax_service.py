from tax_service import total_with_tax


def test_tax_rounds_to_cents():
    assert total_with_tax(19.99, 0.0875) == 21.74
