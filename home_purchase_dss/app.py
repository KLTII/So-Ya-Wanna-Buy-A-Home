import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Home Purchase Decision Dashboard", page_icon="🏠", layout="wide")


def mortgage_payment(principal: float, annual_rate_percent: float, years: int) -> float:
    if principal < 0 or annual_rate_percent < 0 or years <= 0:
        raise ValueError("Invalid loan parameters")
    n = years * 12
    r = annual_rate_percent / 100 / 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** (-n))


st.title("🏠Home Purchase Decision Dashboard")
st.caption("Compare estimated costs of three hypothetical properties. Replace example values with actual quotes and estimates.")

with st.sidebar:
    st.header("Buyer assumptions")
    down_pct = st.slider("Down payment (%)", 0, 50, 20, 5)
    rate = st.number_input("Annual mortgage interest rate (%)", min_value=0.0, max_value=25.0, value=6.5, step=0.25)
    term = st.selectbox("Loan term (years)", [15, 20, 30], index=2)
    tax_pct = st.number_input("Estimated annual property tax (%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    monthly_budget = st.number_input("Monthly housing budget ($)", min_value=0, value=3500, step=100)
    st.caption("Taxes are estimated as a percentage of purchase price. This is a simplified assumption.")

st.subheader("Property details")
defaults = [
    {"name": "Condominium", "price": 350000, "hoa": 425, "insurance": 85, "maintenance": 125},
    {"name": "Townhome", "price": 450000, "hoa": 175, "insurance": 110, "maintenance": 225},
    {"name": "Detached house", "price": 550000, "hoa": 0, "insurance": 160, "maintenance": 400},
]
cols = st.columns(3)
properties = []
for col, item in zip(cols, defaults):
    with col:
        st.markdown(f"#### {item['name']}")
        price = st.number_input("Purchase price ($)", min_value=0, value=item["price"], step=10000, key=f"price_{item['name']}")
        hoa = st.number_input("Monthly HOA ($)", min_value=0, value=item["hoa"], step=25, key=f"hoa_{item['name']}")
        insurance = st.number_input("Monthly insurance ($)", min_value=0, value=item["insurance"], step=10, key=f"ins_{item['name']}")
        maintenance = st.number_input("Monthly maintenance reserve ($)", min_value=0, value=item["maintenance"], step=25, key=f"maint_{item['name']}")
        principal = price * (1 - down_pct / 100)
        payment = mortgage_payment(principal, rate, term)
        tax = price * tax_pct / 100 / 12
        total = payment + tax + hoa + insurance + maintenance
        properties.append({"Property": item["name"], "Price": price, "Down payment": price * down_pct / 100, "Principal & interest": payment, "Property tax": tax, "HOA": hoa, "Insurance": insurance, "Maintenance reserve": maintenance, "Monthly total": total, "Budget status": "Within budget" if total <= monthly_budget else "Over budget"})
        st.metric("Estimated monthly cost", f"${total:,.0f}")
        if total > monthly_budget:
            st.warning("Exceeds your monthly budget")

df = pd.DataFrame(properties)
st.subheader("Monthly cost comparison")
fig = px.bar(df, x="Property", y=["Principal & interest", "Property tax", "HOA", "Insurance", "Maintenance reserve"], barmode="stack", labels={"value": "Monthly cost ($)", "variable": "Cost category"})
fig.update_layout(legend_title_text="Expense", yaxis_tickprefix="$")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Comparison table")
st.dataframe(df.style.format({col: "${:,.2f}" for col in df.columns if col not in ("Property", "Budget status")}), use_container_width=True, hide_index=True)

lowest = df.loc[df["Monthly total"].idxmin()]
st.success(f"Lowest estimated monthly cost: {lowest['Property']} (${lowest['Monthly total']:,.2f}/month). This is a cost comparison, not an overall purchase recommendation.")
st.info("Simplified estimates exclude closing costs, mortgage insurance, utilities, special assessments, appreciation, and tax deductions. HOA obligations and insurance coverage vary by property and ownership structure.")
