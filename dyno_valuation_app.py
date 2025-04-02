import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Function to calculate the present value of terminal EBITDA and revenue NPV
def calculate_present_value(npv, discount_rate, years):
    return npv / ((1 + discount_rate) ** years)

# Function to calculate the blended value
def calculate_blended_value(ebitda_value, revenue_value, weight=0.5):
    return (ebitda_value * weight) + (revenue_value * (1 - weight))

# Streamlit App UI
st.title("Dyno Valuation Model - Business Valuation")

# Inputs
st.header("Inputs")

# FDA Approval Date
approval_date = st.date_input("FDA Approval Date", datetime(2026, 1, 1))

# Ensure the FDA approval date is in datetime format
approval_date = pd.to_datetime(approval_date)

# Lag time (Months) before revenue starts
domestic_lag = st.slider("Lag time (months) for Domestic Hospital Revenue", 0, 24, 6)
international_lag = st.slider("Lag time (months) for International Hospital Revenue", 0, 24, 12)
rpm_lag = st.slider("Lag time (months) for RPM Revenue", 0, 24, 12)

# Discount Rate for all business lines (same for both EBITDA and Revenue)
discount_rate_domestic = st.slider("Discount Rate (Domestic Hospital)", 0.0, 1.0, 0.1)
discount_rate_international = st.slider("Discount Rate (International Hospital)", 0.0, 1.0, 0.15)
discount_rate_rpm = st.slider("Discount Rate (RPM)", 0.0, 1.0, 0.2)

# Actual revenue and EBITDA data for each business line
st.header("Revenue & EBITDA Projections")

# Domestic Revenue and EBITDA (provided)
domestic_revenue = {
    "2025": 0,
    "2026": 5248050,
    "2027": 20719845,
    "2028": 46512630,
    "2029": 94529575
}

domestic_ebitda = {
    "2025": -3804274,
    "2026": 259896,
    "2027": 10043270,
    "2028": 25254228,
    "2029": 55882649
}

# International Revenue and EBITDA (provided)
international_revenue = {
    "2025": 0,
    "2026": 0,
    "2027": 14680170,
    "2028": 64305788,
    "2029": 140999280
}

international_ebitda = {
    "2025": -3494274,
    "2026": -3781015,
    "2027": 5375248,
    "2028": 38243566,
    "2029": 89954378
}

# RPM Revenue and EBITDA (provided)
rpm_revenue = {
    "2025": 0,
    "2026": 0,
    "2027": 689227,
    "2028": 14875721,
    "2029": 37987006
}

rpm_ebitda = {
    "2025": -1730000,
    "2026": -3375000,
    "2027": -1975933,
    "2028": 6261030,
    "2029": 20067330
}

# Display editable tables for inputting data for each business line
st.subheader("Domestic Hospital")
domestic_df = pd.DataFrame(domestic_revenue.items(), columns=["Year", "Revenue"])
domestic_df["EBITDA"] = domestic_df["Year"].map(domestic_ebitda)
st.write(domestic_df)

st.subheader("International Hospital")
international_df = pd.DataFrame(international_revenue.items(), columns=["Year", "Revenue"])
international_df["EBITDA"] = international_df["Year"].map(international_ebitda)
st.write(international_df)

st.subheader("RPM")
rpm_df = pd.DataFrame(rpm_revenue.items(), columns=["Year", "Revenue"])
rpm_df["EBITDA"] = rpm_df["Year"].map(rpm_ebitda)
st.write(rpm_df)

# Now, calculate the present value for each business line

# Calculate NPVs for each business line
years_to_revenue_domestic = (datetime.now() - approval_date).days / 365 + (domestic_lag / 12)
years_to_revenue_international = (datetime.now() - approval_date).days / 365 + (international_lag / 12)
years_to_revenue_rpm = (datetime.now() - approval_date).days / 365 + (rpm_lag / 12)

# Present value calculations for the years 2026 to 2029
present_value_domestic_revenue = {year: calculate_present_value(value, discount_rate_domestic, years_to_revenue_domestic) for year, value in domestic_revenue.items()}
present_value_international_revenue = {year: calculate_present_value(value, discount_rate_international, years_to_revenue_international) for year, value in international_revenue.items()}
present_value_rpm_revenue = {year: calculate_present_value(value, discount_rate_rpm, years_to_revenue_rpm) for year, value in rpm_revenue.items()}

# EBITDA Present value calculations
present_value_domestic_ebitda = {year: calculate_present_value(value, discount_rate_domestic, years_to_revenue_domestic) for year, value in domestic_ebitda.items()}
present_value_international_ebitda = {year: calculate_present_value(value, discount_rate_international, years_to_revenue_international) for year, value in international_ebitda.items()}
present_value_rpm_ebitda = {year: calculate_present_value(value, discount_rate_rpm, years_to_revenue_rpm) for year, value in rpm_ebitda.items()}

# Calculate the total blended value for each business
blended_value_domestic = calculate_blended_value(sum(present_value_domestic_ebitda.values()), sum(present_value_domestic_revenue.values()))
blended_value_international = calculate_blended_value(sum(present_value_international_ebitda.values()), sum(present_value_international_revenue.values()))
blended_value_rpm = calculate_blended_value(sum(present_value_rpm_ebitda.values()), sum(present_value_rpm_revenue.values()))

# Total business value
total_business_value = blended_value_domestic + blended_value_international + blended_value_rpm

# Outputs
st.header("Outputs")
st.write(f"Domestic Business Line Blended Value: ${blended_value_domestic:,.0f}")
st.write(f"International Business Line Blended Value: ${blended_value_international:,.0f}")
st.write(f"RPM Business Line Blended Value: ${blended_value_rpm:,.0f}")
st.write(f"Total Business Value: ${total_business_value:,.0f}")

