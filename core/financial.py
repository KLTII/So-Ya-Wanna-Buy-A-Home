def mortgage_payment(principal, annual_rate, years):
    """
    Calculate the monthly principal-and-interest payment.

    annual_rate must be a decimal:
    6.5% is entered as 0.065.
    """
    if principal < 0:
        raise ValueError("Principal cannot be negative.")

    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if years <= 0:
        raise ValueError("Loan term must be positive.")

    payments = years * 12
    monthly_rate = annual_rate / 12

    if monthly_rate == 0:
        return principal / payments

    return (principal * monthly_rate / (1 - (1 + monthly_rate) ** (-payments)))

def monthly_ownership_cost(price, down_payment_percent, annual_rate, years, annual_property_tax, annual_insurance, monthly_hoa, monthly_maintenance):
    if price < 0:
        raise ValueError("Price cannot be negative.")

    if not 0 <= down_payment_percent <= 100:
        raise ValueError("Down payment must be between 0 - 100%.")

    expenses = [annual_property_tax, annual_insurance, monthly_hoa, monthly_maintenance]

    if any(value < 0 for value in expenses):
        raise ValueError("Expenses cannot be negative.")

    loan_amount = price * (1 - down_payment_percent / 100)
    mortgage = mortgage_payment(loan_amount, annual_rate, years)
    property_tax = annual_property_tax / 12
    insurance = annual_insurance / 12
    total = (mortgage + property_tax + insurance + monthly_hoa + monthly_maintenance)

    return    {
        "Mortgage": mortgage, "Property tax": property_tax, "Insurance": insurance, "HOA": monthly_hoa, "Maintenance": monthly_maintenance, "Total": total
    }