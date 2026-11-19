import pytest
from core.sensitivity import calculate_sensitivity

@pytest.fixture
def sample_properties():
    return [{
        "Property": "Property 1",
        "Price": 350000,
        "Tax": 3600,
        "Insurance": 1200,
        "HOA": 300,
        "Maintenance": 150
    }]
def test_interest_rate_sensitivity(sample_properties):
    result = calculate_sensitivity(
        properties=sample_properties,
        down_payment=20,
        interest_rate=6,
        loan_years=30,
        variable="Interest Rate",
        values=[4, 6, 8]
    )
    assert len(result) == 3
    # Mortgage payments should rise as rates increase
    payments = result["Monthly Mortgage"].tolist()
    assert payments[0] < payments[1] < payments[2]
def test_down_payment_sensitivity(sample_properties):
    result = calculate_sensitivity(
        properties=sample_properties,
        down_payment=20,
        interest_rate=6,
        loan_years=30,
        variable="Down Payment",
        values=[10, 20, 30]
    )
    assert len(result) == 3
    # Mortgage payments should fall as down payment rises
    payments = result["Monthly Mortgage"].tolist()
    assert payments[0] > payments[1] > payments[2]
def test_unsupported_variable(sample_properties):
    with pytest.raises(ValueError):
        calculate_sensitivity(
            properties=sample_properties,
            down_payment=20,
            interest_rate=6,
            loan_years=30,
            variable="Invalid Variable",
            values=[1, 2, 3]
        )
def test_baseline_matches_existing_calculation(sample_properties):
    result = calculate_sensitivity(
        properties=sample_properties,
        down_payment=20,
        interest_rate=6,
        loan_years=30,
        variable="Interest Rate",
        values=[6]
    )
    # 280,000 loan at 6% over 30 years, plus $850 in monthly non-mortgage costs.
    # Mortgage payment: approximately $1,678.74
    # Monthly non-mortgage expenses: $850.00
    # Total monthly cost: approximately $2,528.74
    assert result.iloc[0]["Total Monthly Cost"] == pytest.approx(
        2528.74,
        abs=0.02
    )