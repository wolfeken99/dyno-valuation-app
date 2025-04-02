
import streamlit as st
import pandas as pd

# User Inputs
fda_approval_date = st.date_input("FDA Approval Date", value=pd.to_datetime("2025-12-31"))
domestic_lag = st.slider("Domestic Hospital Lag (months)", 0, 24, 0)
international_lag = st.slider("International Hospital Lag (months)", 0, 24, 12)
rpm_lag = st.slider("RPM Market Lag (months)", 0, 24, 12)

# Revenue & EBITDA Forecasts
data = {
    "Year": [2025, 2026, 2027, 2028, 2029],
    "Domestic_Revenue": [0, 5248050, 20719845, 46512630, 94295745],
    "Domestic_EBITDA": [-3804274, 259896, 10043270, 25254228, 55882649],
    "International_Revenue": [0, 0, 14680170, 64305788, 140999280],
    "International_EBITDA": [-3494274, -3781015, 5375248, 38243566, 89954378],
    "RPM_Revenue": [0, 0, 689227, 14785271, 37897007],
    "RPM_EBITDA": [-1730000, -3375000, -1975933, 6261403, 20067330],
}

df = pd.DataFrame(data)

# Valuation Assumptions
terminal_rev_multiple = st.number_input("Terminal Revenue Multiple", value=4.0)
terminal_ebitda_multiple = st.number_input("Terminal EBITDA Multiple", value=10.0)
discount_rate_domestic = st.slider("Discount Rate - Domestic", 0.0, 1.0, 0.5)
discount_rate_intl = st.slider("Discount Rate - International", 0.0, 1.0, 0.6)
discount_rate_rpm = st.slider("Discount Rate - RPM", 0.0, 1.0, 0.7)

# Calculate Terminal Value (2029)
terminal_values = {
    "Domestic": df["Domestic_EBITDA"].iloc[-1] * terminal_ebitda_multiple,
    "International": df["International_EBITDA"].iloc[-1] * terminal_ebitda_multiple,
    "RPM": df["RPM_EBITDA"].iloc[-1] * terminal_ebitda_multiple,
}

# Discounted Terminal Value back to present using private multiples
def npv(value, years, rate):
    return value / ((1 + rate) ** years)

valuation_results = []
for segment, terminal in terminal_values.items():
    if segment == "Domestic":
        lag = domestic_lag / 12
        rate = discount_rate_domestic
    elif segment == "International":
        lag = international_lag / 12
        rate = discount_rate_intl
    else:
        lag = rpm_lag / 12
        rate = discount_rate_rpm
    years_to_terminal = 2029 - 2025 + lag
    terminal_npv = npv(terminal, years_to_terminal, rate)
    revenue_npv = npv(df[f"{segment}_Revenue"].iloc[-1] * terminal_rev_multiple, years_to_terminal, rate)
    blended = (terminal_npv + revenue_npv) / 2
    valuation_results.append({
        "Segment": segment,
        "Terminal (EBITDA) NPV": terminal_npv,
        "Terminal (Revenue) NPV": revenue_npv,
        "Blended Value": blended
    })

valuation_df = pd.DataFrame(valuation_results)
st.dataframe(valuation_df, use_container_width=True)

# Investor Return Analysis
total_pre_money = valuation_df["Blended Value"].sum()
post_money = total_pre_money + 5_000_000
ownership_pct = 5_000_000 / post_money
exit_value = valuation_df["Blended Value"].sum()
exit_proceeds = exit_value * ownership_pct
moic = exit_proceeds / 5_000_000
irr = ((exit_proceeds / 5_000_000) ** (1/5)) - 1

st.subheader("Investor Return ($5M Entry)")
st.markdown(f"**Pre-Money Valuation:** ${total_pre_money:,.0f}")
st.markdown(f"**Ownership %:** {ownership_pct*100:.2f}%")
st.markdown(f"**Exit Proceeds:** ${exit_proceeds:,.0f}")
st.markdown(f"**MOIC:** {moic:.2fx}")
st.markdown(f"**IRR:** {irr*100:.1f}%")
