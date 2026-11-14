# Python standard library
import sys
import math
import statistics
import decimal
import unittest
# Third-party libraries
import numpy as np
import pandas as pd
import scipy
import matplotlib
import statsmodels
import sklearn
import plotly
import plotly.express as px
import streamlit as st
import pytest
from core.financial import monthly_ownership_cost
from core.financial import mortgage_payment
from core.scoring import (
    affordability_score,
    space_score,
    weighted_score
)

st.set_page_config(page_title="So Ya Wanna Buy A Home", page_icon="", layout="wide")
st.title("So Ya Wanna Buy A Home")

# Initialize stored property data
# OR
# Store the most recently submitted properties
if "properties" not in st.session_state:
    st.session_state.properties = None


# Property input form
property_labels = ["Property 1", "Property 2", "Property 3"]
housing_types = ["Condominium", "Townhome", "Detached House"]
default_prices = [0, 0, 0]
with st.form("property_form"):
    st.header("Enter Property Information")
    # Create 3 columns inside the form
    columns = st.columns(3)
    properties = []
    for i, property_label in enumerate(property_labels):
        with columns[i]:
            st.subheader(property_label)
            listing_url = st.text_input(
                "Property listing URL",
                placeholder="Paste a listing URL",
                key=f"listing_url_{i}"
            )
            # Let users choose the housing type
            housing_type = st.selectbox(
                "Housing type",
                options=housing_types,
                index=i,
                key=f"housing_type_{i}"
            )
            price = st.number_input(
                "Purchase Price ($)",
                min_value=0.0,
                value=float(default_prices[i]),
                step=10000.0,
                key=f"price_{i}"
            )
            tax = st.number_input(
                "Annual property tax ($)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                key=f"tax_{i}"
            )
            insurance = st.number_input(
                "Annual insurance ($)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                key=f"insurance_{i}"
            )
            hoa = st.number_input(
                "Monthly HOA fees ($)",
                min_value=0.0,
                value=0.0,
                step=25.0,
                key=f"hoa_{i}"
            )
            maintenance = st.number_input(
                "Monthly maintenance ($)",
                min_value=0.0,
                value=0.0,
                step=25.0,
                key=f"maintenance_{i}"
            )
            square_feet = st.number_input(
                "Living area (square feet)",
                min_value=1,
                value=1500,
                step=10,
                key=f"square_feet_{i}"
            )
            privacy = st.slider(
                "Privacy rating (1-10)",
                min_value=1,
                max_value=10,
                value=5,
                key=f"privacy_{i}"
            )
            maintenance_ease = st.slider(
                "Maintenance ease (1-10)",
                min_value=1,
                max_value=10,
                value=5,
                key=f"maintenance_ease_{i}"
            )
            # Store each property as a dictionary
            properties.append({
                "Property": property_label,
                "Listing URL": listing_url,
                "Housing Type": housing_type,
                "Price": price,
                "Tax": tax,
                "Insurance": insurance,
                "HOA": hoa,
                "Maintenance": maintenance,
                "Square Feet": square_feet,
                "Privacy": privacy,
                "Maintenance Ease": maintenance_ease
            })
    # One button submits all 3 columns
    submitted = st.form_submit_button("Compare Properties")
    # Save the submitted dictionaries, only when submitted
if submitted:
    st.session_state.properties = properties
# Work with the submitted information, and display submitted property data
if st.session_state.properties is not None:
    st.subheader("Submitted Properties")
    for property_data in st.session_state.properties:
        st.write(
            property_data["Property"],
            f"${property_data["Price"]:,.2f}"
        )
else:
    st.info("Enter property details and click Compare Properties.")

# Property input form
# with st.form("property_form_former"):
#     st.header("Enter Property Information")
#     propert_1_price = st.number_input(
#         "Property 1 price ($)",
#         min_value=0.0,
#         value=350000.0
#     )

#     propert_2_price = st.number_input(
#         "Property 2 price ($)",
#         min_value=0.0,
#         value=350000.0
#     )

#     propert_3_price = st.number_input(
#         "Property 3 price ($)",
#         min_value=0.0,
#         value=350000.0
#     )

#     submitted = st.form_submit_button("property comparison")

# # Save data only when submitted
# if submitted:
#     st.session_state.properties = {
#         "Property 1": propert_1_price,
#         "Property 2": propert_2_price,
#         "Property 3": propert_3_price
#     }

# # Display the submitted property data
# if st.session_state.properties is not None:
#     st.subheader("Submitted Properties")
#     for name, price in st.session_state.properties.items():
#         st.write(f"{name}: ${price:,.2f}")
# else:
#     st.info("Enter property details and click Compare Properties.")

# if st.session_state.properties is not None:
#     st.header("Mortgage Scenario Analysis")
#     interest_rate = st.slider(
#         "Annual interest rate (%)",
#         min_value=0.0,
#         max_value=15.0,
#         value=6.5,
#         step=0.25
#     )
#     down_payment = st.slider(
#         "Down Payment (%)",
#         min_value=0,
#         max_value=100,
#         value=20,
#         step=5
#     )
#     loan_years = st.selectbox(
#         "Mortgage term (years)",
#         options=[10, 15, 20, 25, 30],
#         index=4
#     )
#     st.subheader("Monthly Mortgage Payments")
#     for property_data in st.session_state.properties:
#         # Retrieve the price for this specific property
#         price = property_data["Price"]
#         # Calculate the mortgage principal
#         principal = price * (1 - down_payment / 100)
#         # Calculate the monthly mortgage payment
#         payment = mortgage_payment(
#             principal=principal,
#             annual_rate=interest_rate / 100,
#             years=loan_years
#         )
#         # Display the result
#         st.metric(
#             label=(
#                 f"{property_data['Property']} "
#                 f"({property_data['Housing Type']})"
#             ),
#             value=f"${payment:,.2f}"
#         )

# Beginning of non-form format
st.write("Compare 3 properties based on their estimated monthly ownership costs.")

st.sidebar.header("Buyer Information")
down_payment = st.sidebar.slider(
    "Down payment (%)",
    min_value=0,
    max_value=100,
    value=20,
    step=5
)
interest_rate = st.sidebar.number_input(
    "Annual interest rate (%)",
    min_value=0.0,
    max_value=25.0,
    value=6.5,
    step=0.25
)
loan_years = st.sidebar.selectbox(
    "Mortgage term (years)",
    options=[10, 15, 20, 25, 30],
    index=4
)
# loan_years = st.sidebar.number_input(
#     "Mortgage term (years)",
#     min_value=0,
#     max_value=30,
#     value=30,
#     step=1
# )
monthly_budget = st.sidebar.number_input(
    "Maximum monthly housing budget ($)",
    min_value=0.0,
    value=3500.0,
    step=100.0
)

st.sidebar.header("Buyer Preferences")
desired_square_feet = st.sidebar.number_input(
    "Desired living area (sq ft)",
    min_value=100,
    value=1800,
    step=100
)
st.sidebar.subheader("Importance Weights")
affordability_weight = st.sidebar.slider(
    "Affordability importance",
    min_value=1,
    max_value=10,
    value=5
)
space_weight = st.sidebar.slider(
    "Living space importance",
    min_value=1,
    max_value=10,
    value=5
)
privacy_weight = st.sidebar.slider(
    "Privacy importance",
    min_value=1,
    max_value=10,
    value=5
)
maintenance_weight = st.sidebar.slider(
    "Maintenance ease importance",
    min_value=1,
    max_value=10,
    value=5
)
weights = {
    "Affordability": affordability_weight,
    "Living Space": space_weight,
    "Privacy": privacy_weight,
    "Maintenance Ease": maintenance_weight
}

st.header("Financial Comparison")
# if st.session_state.properties is not None:
results = []
cost_breakdowns = []
for property_data in properties:
    # Calculate monthly ownership cost
    costs = monthly_ownership_cost(
        price=property_data["Price"],
        down_payment_percent=down_payment,
        annual_rate=interest_rate / 100,
        years=loan_years,
        annual_property_tax=property_data["Tax"],
        annual_insurance=property_data["Insurance"],
        monthly_hoa=property_data["HOA"],
        monthly_maintenance=property_data["Maintenance"]
    )
    results.append({
        "Property": property_data["Property"],
        "Housing Type": property_data["Housing Type"],
        "Purchase Price": property_data["Price"],
        "Monthly Mortgage": costs["Mortgage"],
        "Total Monthly Cost": costs["Total"],
        "Within Budget": costs["Total"] <= monthly_budget
    })
    cost_breakdowns.append({
        "Property": property_data["Property"],
        **costs
    })
    

results_df = pd.DataFrame(results)

if sum(weights.values()) == 0:
    st.warning("Set at least one importance weight above zero.")
    st.stop()
    
st.header("Buyer Preference Scoring")
scoring_results = []
for property_data in properties:
    # Calculate monthly ownership cost
    costs = monthly_ownership_cost(
        price=property_data["Price"],
        down_payment_percent=down_payment,
        annual_rate=interest_rate / 100,
        years=loan_years,
        annual_property_tax=property_data["Tax"],
        annual_insurance=property_data["Insurance"],
        monthly_hoa=property_data["HOA"],
        monthly_maintenance=property_data["Maintenance"]
    )
    # Calculate criterion scores
    scores = {
        "Affordability": affordability_score(
            costs["Total"],
            monthly_budget
        ),
        "Living Space": space_score(
            property_data["Square Feet"],
            desired_square_feet
        ),
        "Privacy": property_data["Privacy"] * 10,
        "Maintenance Ease": (property_data["Maintenance Ease"] * 10)
    }
    # Calculate weighted total
    total_score = weighted_score(scores, weights)
    scoring_results.append({
        "Property": property_data["Property"],
        "Housing Type": property_data["Housing Type"],
        "Monthly Cost": costs["Total"],
        "Within Budget": costs["Total"] <= monthly_budget,
        ** scores,
        "Overall Score": total_score
    })
scoring_df = pd.DataFrame(scoring_results)
# Sort properties by overall score
scoring_df = scoring_df.sort_values(
    by="Overall Score",
    ascending=False
)
st.dataframe(
    scoring_df,
    hide_index=True,
    width="stretch"
)

st.subheader("Overall Property Scores")
fig = px.bar(
    scoring_df,
    x="Property",
    y="Overall Score",
    color="Housing Type",
    text="Overall Score",
    title="Weighted Property Comparison"
)
fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)
fig.update_yaxes(range=[0, 110])
st.plotly_chart(fig, width="stretch")

st.subheader("Property Recommendation")
if sum(weights.values()) == 0:
    st.warning(
        "Select at least one importance weight above zero."
    )
else:
    affordability_properties = scoring_df[scoring_df["Within Budget"]]
    if affordability_properties.empty:
        st.warning(
            "None of the properties meet your monthly budget. "
            "Review your options before making a decision."
        )
    else:
        best_property = affordability_properties.iloc[0]
        st.success(
            f"Based on your preferences, "
            f"{best_property['Property']} "
            f"({best_property['Housing Type']}) "
            f"is your highest scoring property within budget, "
            f"with a score of "
            f"{best_property['Overall Score']:.1f}/100"
        )

costs_df = pd.DataFrame(cost_breakdowns)

summary_columns = st.columns(3)

for i, result in enumerate(results):
    with summary_columns[i]:
        st.metric(
            label=(
                f"{result["Property"]} "
                f"({result["Housing Type"]})"
            ),
            value=f"${result['Total Monthly Cost']:,.2f}",
            delta=(
                "Within budget"
                if result["Within Budget"]
                else "Over budget"
            ),
            delta_color="off"
        )

st.subheader("Property Comparison Table")
st.dataframe(
    results_df,
    hide_index=True,
    width="stretch"
)

st.subheader("Monthly Cost Breakdown")

chart_data = costs_df.melt(
    id_vars="Property",
    value_vars=[
        "Mortgage",
        "Property tax",
        "Insurance",
        "HOA",
        "Maintenance"
    ],
    var_name="Expense",
    value_name="Monthly Cost"
)

fig = px.bar(
    chart_data,
    x="Property",
    y="Monthly Cost",
    color="Expense",
    barmode="stack",
    title="Estimated Monthly Ownership Costs"
)

fig.update_layout(
    yaxis_title = "Monthly Cost ($)",
    xaxis_title = "Housing Type"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.header("Decision Guidance")

affordable = results_df[
    results_df["Within Budget"]
]

if affordable.empty:
    st.warning("None of the properties meet your monthly housing budget.")
else:
    cheapest = affordable.loc[
        affordable["Total Monthly Cost"].idxmin()
    ]
    st.success(
        f"The lowest cost property within your budget is "
        f"the {cheapest['Property']}, with an estimated "
        f"monthly cost of "
        f"${cheapest['Total Monthly Cost']:,.2f}."
    )

st.info(
    "These estimates exclude PMI, utilities, closing costs, "
    "and other potential ownership expenses. "
    "The lowest cost property is not necessarily the best "
    "overall choice."
)

# form1.header("3 options to choose from")
# home1 = form1.text_input("Enter the 1st property you're interested in")
# home2 = form1.text_input("Enter the 2nd property you're interested in")
# home3 = form1.text_input("Enter the 3rd property you're interested in")
st.write("3 options to choose from")
with st.form(key="option1"):
    home1 = st.text_input("Enter the 1st property you're interested in", key="h1")
    purchasePrice1 = st.text_input("Enter the purchase price")
    downPayment1 = st.text_input("Enter the down payment amount")
    closingCosts1 = st.text_input("Enter the closing costs")
    yearBuilt1 = st.text_input("Enter the year built")
    propertyTaxRate1 = st.text_input("Enter the property tax rate")
    insurance1 = st.text_input("Enter the monthly insurance cost")
    hoa1 = st.text_input("Enter the monthly HOA fee")
    electricity1 = st.text_input("Enter the monthly cost for electricity")
    water1 = st.text_input("Enter the monthly cost for water")
    sewer1 = st.text_input("Enter the monthly cost for sewer")
    garbage1 = st.text_input("Enter the monthly cost for garbage")
    gas1 = st.text_input("Enter the monthly cost for gas")
    entered1 = st.form_submit_button("Enter")
with st.form(key="option2"):
    home2 = st.text_input("Enter the 2nd property you're interested in", key="h2")
    purchasePrice2 = st.text_input("Enter the purchase price")
    downPayment2 = st.text_input("Enter the down payment amount")
    closingCosts2 = st.text_input("Enter the closing costs")
    yearBuilt2 = st.text_input("Enter the year built")
    propertyTaxRate2 = st.text_input("Enter the property tax rate")
    insurance2 = st.text_input("Enter the monthly insurance cost")
    hoa2 = st.text_input("Enter the monthly HOA fee")
    electricity2 = st.text_input("Enter the monthly cost for electricity")
    water2 = st.text_input("Enter the monthly cost for water")
    sewer2 = st.text_input("Enter the monthly cost for sewer")
    garbage2 = st.text_input("Enter the monthly cost for garbage")
    gas2 = st.text_input("Enter the monthly cost for gas")
    entered2 = st.form_submit_button("Enter")
with st.form(key="option3"):
    home3 = st.text_input("Enter the 3rd property you're interested in", key="h3")
    purchasePrice3 = st.text_input("Enter the purchase price")
    downPayment3 = st.text_input("Enter the down payment amount")
    closingCosts3 = st.text_input("Enter the closing costs")
    yearBuilt3 = st.text_input("Enter the year built")
    propertyTaxRate3 = st.text_input("Enter the property tax rate")
    insurance3 = st.text_input("Enter the monthly insurance cost")
    hoa3 = st.text_input("Enter the monthly HOA fee")
    electricity3 = st.text_input("Enter the monthly cost for electricity")
    water3 = st.text_input("Enter the monthly cost for water")
    sewer3 = st.text_input("Enter the monthly cost for sewer")
    garbage3 = st.text_input("Enter the monthly cost for garbage")
    gas3 = st.text_input("Enter the monthly cost for gas")
    entered3 = st.form_submit_button("Enter")
with st.form(key="generals"):
    interestRate = st.text_input("Enter the interest rate")
    loanTerm = st.text_input("Enter the loan term")
    internet = st.text_input("Enter the monthly cost for internet")
entered4 = st.button("Enter")
form1 = st.form(key="3 options")
if entered1:
    form1.write(f"Property 1:  {home1}")
    form1.write(f"Purchase Price:  {purchasePrice1}")
    form1.write(f"Down Payment Amount:  {downPayment1}")
    form1.write(f"Closing Costs:  {closingCosts1}")
    form1.write(f"Year Built:  {yearBuilt1}")
    form1.write(f"Property Tax:  {propertyTaxRate1}")
    form1.write(f"Insurance:  {insurance1}")
    form1.write(f"HOA fee:  {hoa1}")
    form1.write(f"Electricity:  {electricity1}")
    form1.write(f"Water:  {water1}")
    form1.write(f"Sewer:  {sewer1}")
    form1.write(f"Garbage:  {garbage1}")
    form1.write(f"Gas:  {gas1}")

if entered2:
    form1.write(f"Property 2:  {home2}")
    form1.write(f"Purchase Price:  {purchasePrice2}")
    form1.write(f"Down Payment Amount:  {downPayment2}")
    form1.write(f"Closing Costs:  {closingCosts2}")
    form1.write(f"Year Built:  {yearBuilt2}")
    form1.write(f"Property Tax:  {propertyTaxRate2}")
    form1.write(f"Insurance:  {insurance2}")
    form1.write(f"HOA fee:  {hoa2}")
    form1.write(f"Electricity:  {electricity2}")
    form1.write(f"Water:  {water2}")
    form1.write(f"Sewer:  {sewer2}")
    form1.write(f"Garbage:  {garbage2}")
    form1.write(f"Gas:  {gas2}")

if entered3:
    form1.write(f"Property 3:  {home3}")
    form1.write(f"Purchase Price:  {purchasePrice3}")
    form1.write(f"Down Payment Amount:  {downPayment3}")
    form1.write(f"Closing Costs:  {closingCosts3}")
    form1.write(f"Year Built:  {yearBuilt3}")
    form1.write(f"Property Tax:  {propertyTaxRate3}")
    form1.write(f"Insurance:  {insurance3}")
    form1.write(f"HOA fee:  {hoa3}")
    form1.write(f"Electricity:  {electricity3}")
    form1.write(f"Water:  {water3}")
    form1.write(f"Sewer:  {sewer3}")
    form1.write(f"Garbage:  {garbage3}")
    form1.write(f"Gas:  {gas3}")

if entered4:
    form1.write(f"Interest Rate:  {interestRate}")
    form1.write(f"Loan Term:  {loanTerm}")
    form1.write(f"Internet:  {internet}")

def mortgage_payment(principal, annual_rate, years):
    if principal < 0 or annual_rate < 0 or years <= 0:
        raise ValueError("Invalid mortgage parameters")
    n = years * 12
    r = annual_rate / 12
    if r == 0:
        return principal / n
    growth = math.pow(1 + r, n)
    return principal * r * growth / (growth - 1)

# purchasePrice1Int = int(purchasePrice1)
# interestRateInt = int(interestRate)
# loanTermInt = int(loanTerm)
# payment1 = mortgage_payment(principal=purchasePrice1Int, annual_rate=interestRateInt, years=loanTermInt)
# st.write(f"Monthly payment 1: ${payment1:,.2f}")

payment = mortgage_payment(principal=100, annual_rate=0.05, years=30)
st.write(f"Monthly payment: ${payment:,.2f}")



button1 = st.button("Click Me")
if button1:
    st.write("This is some text")

st.header("Start of the Checkbox Section")
like = st.checkbox("Do you like this app?")
button2 = st.button("Submit")
if button2:
    if like:
        st.write("Thanks.  I like it too.")
    else:
        st.write("I'm sorry.  You have bad tastes.")

st.header("Start of the Radio Button Section")
animal = st.radio("What animal is your favourite?", ("Lion", "Tiger", "Bear"))
button3 = st.button("Submit Animal")
if button3:
    st.write(animal)
    if animal == "Lion":
        st.write("ROAR!")

st.header("Start of the Selectbox Section")
animal2 = st.selectbox("What animal is your favourite?", ("Lion", "Tiger", "Bear"))
button4 = st.button("Submit Animal 2")
if button4:
    st.write(animal2)
    if animal2 == "Lion":
        st.write("ROAR!")

st.header("Start of the Multiselect Section")
options = st.multiselect("What animals do you like?", ["Lion", "Tiger", "Bear"])
button5 = st.button("Print Animals")
if button5:
    st.write(options)

st.header("Start of the Slider Section")
epochs_num = st.slider("How many epochs?", 1, 100, 10)
if st.button("Slider Button"):
    st.write(epochs_num)

st.header("Start of the Text Input Section")
user_text = st.text_input("What's your favourite movie?", "Star Wars")
if st.button("Text button"):
    st.write(int(user_text))

user_num = st.number_input("What's your favourite number?")
if st.button("Number Button"):
    st.write(user_num)

def run_sentiment_analysis(txt):
    st.write(f"Analysis Done. {txt}")
txt = st.text_area('Text to analyze', '''Quarterbacks Kirk Cousins (Atlanta to Las Vegas), Kyler Murray (Arizona to Minnesota), Tua Tagovailoa (Miami to Atlanta), and Malik Willis (Green Bay to Miami)''')
st.write('Sentiment:', run_sentiment_analysis(txt))
