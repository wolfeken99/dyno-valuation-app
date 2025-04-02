import streamlit as st
import pandas as pd
from datetime import datetime

# Function to calculate the present value (PV) using a given discount rate and years
def calculate_present_value(value, discount_rate, years):
    return value / ((1 + discount_rate) ** years)

# Function to calculate the business value using Revenue or EBITDA multiples
def calculate_business_value(revenue_or_ebit, multiple):
    return revenue_or_ebit * multiple

# Streamlit App UI
st.title("Dyno Valuation Model - Business Valuation")

# Inputs
st.header("Inputs")

# FDA Approval Date
approval_date = st.date_input("FDA Approval Date", datetime(2026, 1, 1))
approval_date = pd.to_datetime(approval_date)

# Lag time (Months) before revenue starts
domestic_lag = st.slider("Lag time (months) for Domestic Hospital Revenue", 0, 24, 6)
international_lag = st.slider("Lag time (months) for International Hospital Revenue", 0, 24, 12)
rpm_lag = st.slider("Lag time (months) for RPM Revenue", 0, 24, 12)

# Discount Rate for all business lines (same for both EBITDA and Revenue)
discount_rate_domestic = st.slider("Discount Rate (Domestic Hospital)", 0.0, 1.0, 0.1)
discount_rate_international = st.slider("Discount Rate (International Hospital)", 0.0, 1.0, 0.15)
discount_rate_rpm = st.slider("Discount Rate (RPM)", 0.0, 1.0, 0.2)

# Multiples for EV (Enterprise Value), Revenue, and EBITDA
revenue_multiple_domestic = st.number_input("Revenue Multiple (Domestic Hospital)", 0.0, 10.0, 5.0)
ebit_multiple_domestic = st.number_input("EBITDA Multiple (Domestic Hospital)", 0.0, 10.0, 8.0)

revenue_multiple_international = st.number_input("Revenue Multiple (International Hospital)", 0.0, 10.0, 5.0)
ebit_multiple_international = st.number_input("EBITDA Multiple (International Hospital)", 0.0, 10.0, 8.0)

revenue_multiple_rpm = st.number_input("Revenue Multiple (RPM)", 0.0, 10.0, 5.0)
ebit_multiple_rpm = st.number_input("EBITDA Multiple (RPM)", 0.0, 10.0, 8.0)

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

# Calculate NPVs for each business line

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

# Calculate the business value for each business using multiples (Revenue or EBITDA)
business_value_domestic_revenue = calculate_business_value(sum(present_value_domestic_revenue.values()), revenue_multiple_domestic)
business_value_domestic_ebitda = calculate_business_value(sum(present_value_domestic_ebitda.values()), ebit_multiple_domestic)

business_value_international_revenue = calculate_business_value(sum(present_value_international_revenue.values()), revenue_multiple_international)
business_value_international_ebitda = calculate_business_value(sum(present_value_international_ebitda.values()), ebit_multiple_international)

business_value_rpm_revenue = calculate_business_value(sum(present_value_rpm_revenue.values()), revenue_multiple_rpm)
business_value_rpm_ebitda = calculate_business_value(sum(present_value_rpm_ebitda.values()), ebit_multiple_rpm)

# Calculate the total business value
total_business_value = business_value_domestic_revenue + business_value_domestic_ebitda + business_value_international_revenue + business_value_international_ebitda + business_value_rpm_revenue + business_value_rpm_ebitda

# Outputs
st.header("Outputs")
st.write(f"Domestic Business Line Revenue Based Value: ${business_value_domestic_revenue:,.0f}")
st.write(f"Domestic Business Line EBITDA Based Value: ${business_value_domestic_ebitda:,.0f}")
st.write(f"International Business Line Revenue Based Value: ${business_value_international_revenue:,.0f}")
st.write(f"International Business Line EBITDA Based Value: ${business_value_international_ebitda:,.0f}")
st.write(f"RPM Business Line Revenue Based Value: ${business_value_rpm_revenue:,.0f}")
st.write(f"RPM Business Line EBITDA Based Value: ${business_value_rpm_ebitda:,.0f}")
st.write(f"Total Business Value: ${total_business_value:,.0f}")

