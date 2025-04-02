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

# Editable revenue projections for each year (2026-2029)
st.header("Revenue Projections")
domestic_revenue_2026 = st.number_input("Domestic Revenue 2026", min_value=0, value=5248050)
domestic_revenue_2027 = st.number_input("Domestic Revenue 2027", min_value=0, value=20719845)
domestic_revenue_2028 = st.number_input("Domestic Revenue 2028", min_value=0, value=46512630)
domestic_revenue_2029 = st.number_input("Domestic Revenue 2029", min_value=0, value=94529575)

international_revenue_2027 = st.number_input("International Revenue 2027", min_value=0, value=14680170)
international_revenue_2028 = st.number_input("International Revenue 2028", min_value=0, value=64305788)
international_revenue_2029 = st.number_input("International Revenue 2029", min_value=0, value=140999280)

rpm_revenue_2027 = st.number_input("RPM Revenue 2027", min_value=0, value=689227)
rpm_revenue_2028 = st.number_input("RPM Revenue 2028", min_value=0, value=14875721)
rpm_revenue_2029 = st.number_input("RPM Revenue 2029", min_value=0, value=37987006)

# Editable EBITDA margins for each business
st.header("EBITDA Assumptions")
ebitda_margin_domestic = st.slider("EBITDA Margin (Domestic Hospital)", 0.0, 1.0, 0.2)
ebitda_margin_international = st.slider("EBITDA Margin (International Hospital)", 0.0, 1.0, 0.2)
ebitda_margin_rpm = st.slider("EBITDA Margin (RPM)", 0.0, 1.0, 0.2)

# Calculate Present Value for each business line
# Ensure correct handling of months-to-years conversion
years_to_revenue_domestic = (datetime.now() - approval_date).days / 365 + (domestic_lag / 12)
years_to_revenue_international = (datetime.now() - approval_date).days / 365 + (international_lag / 12)
years_to_revenue_rpm = (datetime.now() - approval_date).days / 365 + (rpm_lag / 12)

# Calculate NPVs based on the provided revenue projections
present_value_domestic_revenue = calculate_present_value(domestic_revenue_2026, discount_rate_domestic, years_to_revenue_domestic)
present_value_international_revenue = calculate_present_value(international_revenue_2027, discount_rate_international, years_to_revenue_international)
present_value_rpm_revenue = calculate_present_value(rpm_revenue_2027, discount_rate_rpm, years_to_revenue_rpm)

# Calculate EBITDA NPVs using the provided EBITDA margins
npv_terminal_domestic_ebitda = domestic_revenue_2026 * ebitda_margin_domestic
npv_terminal_international_ebitda = international_revenue_2027 * ebitda_margin_international
npv_terminal_rpm_ebitda = rpm_revenue_2027 * ebitda_margin_rpm

# Present values for EBITDA
present_value_domestic_ebitda = calculate_present_value(npv_terminal_domestic_ebitda, discount_rate_domestic, years_to_revenue_domestic)
present_value_international_ebitda = calculate_present_value(npv_terminal_international_ebitda, discount_rate_international, years_to_revenue_international)
present_value_rpm_ebitda = calculate_present_value(npv_terminal_rpm_ebitda, discount_rate_rpm, years_to_revenue_rpm)

# Calculate blended value for each business line
blended_value_domestic = calculate_blended_value(present_value_domestic_ebitda, present_value_domestic_revenue)
blended_value_international = calculate_blended_value(present_value_international_ebitda, present_value_international_revenue)
blended_value_rpm = calculate_blended_value(present_value_rpm_ebitda, present_value_rpm_revenue)

# Total business value (sum of all business lines)
total_business_value = blended_value_domestic + blended_value_international + blended_value_rpm

# Outputs
st.header("Outputs")

# Display blended values and total business value
st.write(f"Domestic Business Line Blended Value: ${blended_value_domestic:,.0f}")
st.write(f"International Business Line Blended Value: ${blended_value_international:,.0f}")
st.write(f"RPM Business Line Blended Value: ${blended_value_rpm:,.0f}")
st.write(f"Total Business Value: ${total_business_value:,.0f}")

