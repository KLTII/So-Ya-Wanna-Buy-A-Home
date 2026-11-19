import pandas as pd
from core.financial import monthly_ownership_cost

def calculate_sensitivity(
        properties,
        down_payment,
        interest_rate,
        loan_years,
        variable,
        values
):
    """
    Recalculate ownership costs for multiple properties
    while varying one financial assumption.
    
    interest_rate is expressed as a percentage, i.e. 6.5.
    down_payment is also a percentage, i.e. 20.
    """

    if variable not in ("Interest Rate", "Down Payment"):
        raise ValueError("Unsupported sensitivity variable.")
    results = []
    for property_data in properties:
        for value in values:
            scenario_down_payment = down_payment
            scenario_interest_rate = interest_rate
            if variable == "Interest Rate":
                scenario_interest_rate = float(value)
            elif variable == "Down Payment":
                scenario_down_payment = float(value)
            costs = monthly_ownership_cost(
                price=property_data["Price"],
                down_payment_percent=scenario_down_payment,
                annual_rate=scenario_interest_rate / 100,
                years=loan_years,
                annual_property_tax=property_data["Tax"],
                annual_insurance=property_data["Insurance"],
                monthly_hoa=property_data["HOA"],
                monthly_maintenance=property_data["Maintenance"]
            )
            results.append({
                "Property": property_data["Property"],
                "Variable": variable,
                "Value": float(value),
                "Monthly Mortgage": costs["Mortgage"],
                "Total Monthly Cost": costs["Total"]
            })
    return pd.DataFrame(results)