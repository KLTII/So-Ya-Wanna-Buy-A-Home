import pytest
from core.scoring import(
    affordability_score,
    space_score,
    weighted_score
)

def test_affordability_score():
    assert affordability_score(2000, 4000) == 50

def test_over_budget_score():
    assert affordability_score(4500, 4000) == 0

def test_space_score():
    assert space_score(1500, 2000) == 75

def test_space_score_capped():
    assert space_score(2500, 2000) == 100

def test_weighted_score():
    scores = {
        "Affordability": 80,
        "Living Space": 60,
        "Privacy": 90,
        "Maintenance": 70
    }
    weights = {
        "Affordability": 10,
        "Living Space": 5,
        "Privacy": 5,
        "Maintenance Ease": 0
    }
    result = weighted_score(scores, weights)
    assert result == pytest.approx(77.5)

def test_zero_weights():
    scores = {"Affordability": 80}
    weights = {"Affordability": 0}
    with pytest.raises(ValueError):
        weighted_score(scores, weights)