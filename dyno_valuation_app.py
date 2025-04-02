import streamlit as st
import pandas as pd
from datetime import datetime

# Step 1: Inputs from the User
st.title("Dyno Valuation Model")

# FDA Approval Date (input)
approval_date = st.date_input("FDA Approval Date", datetime(2026, 1, 1))

# Lag Time (Months for each Business Line)
lag_time_domestic = st.slider("Lag Time for Domestic Revenue (months)", 0, 24, 6)
lag_time_international = st.slider("Lag Time for International Revenue (months)", 0, 24, 12)
lag_time_rpm = st.slider("Lag Time for RPM Revenue (months)", 0, 24, 12)

# Discount Rates for each Business Line (user-defined)
discount_rate_domestic = st.slider("Discount Rate (Domestic)", 0.0, 1.0, 0.10)
discount_rate_international = st.slider("Discount Rate (International)", 0.0, 1.0, 0.15)
discount_rate_rpm = st.slider("Discount Rate (RPM)", 0.0, 1.0, 0.20)

# Revenue and EBITDA Inputs for each business line (Editable per year)
st.subheader("Domestic Business Line Revenue & EBITDA")
domestic_revenue_2026 = st.number_input("Domestic Revenue 2026", value=5248050, format="%.0f")
domestic_revenue_2027 = st.number_input("Domestic Revenue 2027", value=20719845, format="%.0f")
domestic_revenue_2028 = st.number_input("Domestic Revenue 2028", value=46512630, format="%.0f")
domestic_revenue_2029 = st.number_input("Domestic Revenue 2029", value=94529575, format="%.0f")

domestic_ebitda_2026 = st.number_input("Domestic EBITDA 2026", value=259896, format="%.0f")
domestic_ebitda_2027 = st.number_input("Domestic EBITDA 2027", value=10043270, format="%.0f")
domestic_ebitda_2028 = st.number_input("Domestic EBITDA 2028", value=25254228, format="%.0f")
domestic_ebitda_2029 = st.number_input("Domestic EBITDA 2029", value=55882649, format="%.0f")

# (Repeat the above inputs for International and RPM Business Lines)
# I will not repeat the same code for the International and RPM Business Lines here for brevity.

# Step 2: Business Line Calculations
def calculate_present_value(revenue, ebitda, discount_rate, years_lag):
    years_to_revenue = (datetime.now() - approval_date).days / 365 + years_lag
    discounted_revenue = sum([revenue / (1 + discount_rate) ** i for i in range(1, 6)])
    discounted_ebitda = sum([ebitda / (1 + discount_rate) ** i for i in range(1, 6)])
    return discounted_revenue, discounted_ebitda

# Call the function for Domestic Business
domestic_revenue_value, domestic_ebitda_value = calculate_present_value(
    domestic_revenue_2026, domestic_ebitda_2026, discount_rate_domestic, lag_time_domestic)

# (Repeat calculations for International and RPM using similar functions)

# Step 3: Display the Results in a Table
# Results will show total revenue, EBITDA, and discounted values for each business line
results_df = pd.DataFrame({
    'Business Line': ['Domestic', 'International', 'RPM'],
    'Total Revenue': [domestic_revenue_value, international_revenue_value, rpm_revenue_value],
    'Total EBITDA': [domestic_ebitda_value, international_ebitda_value, rpm_ebitda_value],
})

st.table(results_df)

# Step 4: Total Business Value & MOIC Calculation
total_value = domestic_revenue_value + international_revenue_value + rpm_revenue_value
invested_amount = st.number_input("Invested Amount ($)", value=5000000)

moic = total_value / invested_amount
st.subheader(f"Total Business Value: ${total_value:,.0f}")
st.subheader(f"MOIC (Multiple on Invested Capital): {moic:.2f}")
