import pytest

from core.financial import (mortgage_payment, monthly_ownership_cost)

def test_standard_mortgage():
    result = mortgage_payment(300000, 0.06, 30)
    assert result == pytest.approx(1798.65, abs=0.01)

def test_zero_interest():
    result = mortgage_payment(360000, 0, 30)
    assert result == pytest.approx(1000.0, abs=0.01)

def  test_invalid_term():
    with pytest.raises(ValueError):
        mortgage_payment(300000, 0.06, 0)

def test_monthly_cost():
    result = monthly_ownership_cost    (
        price=350000,
        down_payment_percent=20,
        annual_rate=0.06,
        years=30,
        annual_property_tax=3600,
        annual_insurance=1200,
        monthly_hoa=300,
        monthly_maintenance=150
    )
    assert result["Total"] == pytest.approx(result["Mortgage"] + 850, abs=0.01)