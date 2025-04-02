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

# Editable tables for each business line (Revenue and EBITDA)
st.subheader("Domestic Hospital")
domestic_revenue = {
    "2025": st.number_input("Domestic Revenue 2025", min_value=0, value=0),
    "2026": st.number_input("Domestic Revenue 2026", min_value=0, value=5248050),
    "2027": st.number_input("Domestic Revenue 2027", min_value=0, value=20719845),
    "2028": st.number_input("Domestic Revenue 2028", min_value=0, value=46512630),
    "2029": st.number_input("Domestic Revenue 2029", min_value=0, value=94529575)
}

domestic_ebitda = {
    "2025": st.number_input("Domestic EBITDA 2025", min_value=0, value=-3804274),
    "2026": st.number_input("Domestic EBITDA 2026", min_value=0, value=259896),
    "2027": st.number_input("Domestic EBITDA 2027", min_value=0, value=10043270),
    "2028": st.number_input("Domestic EBITDA 2028", min_value=0, value=25254228),
    "2029": st.number_input("Domestic EBITDA 2029", min_value=0, value=55882649)
}

# International Revenue and EBITDA
st.subheader("International Hospital")
international_revenue = {
    "2025": st.number_input("International Revenue 2025", min_value=0, value=0),
    "2026": st.number_input("International Revenue 2026", min_value=0, value=0),
    "2027": st.number_input("International Revenue 2027", min_value=0, value=14680170),
    "2028": st.number_input("International Revenue 2028", min_value=0, value=64305788),
    "2029": st.number_input("International Revenue 2029", min_value=0, value=140999280)
}

international_ebitda = {
    "2025": st.number_input("International EBITDA 2025", min_value=0, value=-3494274),
    "2026": st.number_input("International EBITDA 2026", min_value=0, value=-3781015),
    "2027": st.number_input("International EBITDA 2027", min_value=0, value=5375248),
    "2028": st.number_input("International EBITDA 2028", min_value=0, value=38243566),
    "2029": st.number_input("International EBITDA 2029", min_value=0, value=89954378)
}

# RPM Revenue and EBITDA
st.subheader("RPM")
rpm_revenue = {
    "2025": st.number_input("RPM Revenue 2025", min_value=0, value=0),
    "2026": st.number_input("RPM Revenue 2026", min_value=0, value=0),
    "2027": st.number_input("RPM Revenue 2027", min_value=0, value=689227),
    "2028": st.number_input("RPM Revenue 2028", min_value=0, value=14875721),
    "2029": st.number_input("RPM Revenue 2029", min_value=0, value=37987006)
}

rpm_ebitda = {
    "2025": st.number_input("RPM EBITDA 2025", min_value=0, value=-1730000),
    "2026": st.number_input("RPM EBITDA 2026", min_value=0, value=-3375000),
    "2027": st.number_input("RPM EBITDA 2027", min_value=0, value=-1975933),
    "2028": st.number_input("RPM EBITDA 2028", min_value=0, value=6261030),
    "2029": st.number_input("RPM EBITDA 2029", min_value=0, value=20067330)
}

# Combine the data into dataframes for display
domestic_df = pd.DataFrame({"Year": list(domestic_revenue.keys()), "Revenue": list(domestic_revenue.values()), "EBITDA": list(domestic_ebitda.values())})
international_df = pd.DataFrame({"Year": list(international_revenue.keys()), "Revenue": list(international_revenue.values()), "EBITDA": list(international_ebitda.values())})
rpm_df = pd.DataFrame({"Year": list(rpm_revenue.keys()), "Revenue": list(rpm_revenue.values()), "EBITDA": list(rpm_ebitda.values())})

# Display tables for each business line
st.subheader("Domestic Hospital Projections")
st.write(domestic_df)

st.subheader("International Hospital Projections")
st.write(international_df)

st.subheader("RPM Projections")
st.write(rpm_df)

# Calculate Present Value (PV) for each business line
def calculate_pv_for_business(revenue, ebitda, discount_rate, years_to_revenue):
    pv_revenue = {year: calculate_present_value(value, discount_rate, years_to_revenue) for year, value in revenue.items()}
    pv_ebitda = {year: calculate_present_value(value, discount_rate, years_to_revenue) for year, value in ebitda.items()}
    return pv_revenue, pv_ebitda

# Calculate the present value of revenue and EBITDA for each business line
years_to_revenue_domestic = (datetime.now() - approval_date).days / 365 + (domestic_lag / 12)
years_to_revenue_international = (datetime.now() - approval_date).days / 365 + (international_lag / 12)
years_to_revenue_rpm = (datetime.now() - approval_date).days / 365 + (rpm_lag / 12)

pv_domestic_revenue, pv_domestic_ebitda = calculate_pv_for_business(domestic_revenue, domestic_ebitda, discount_rate_domestic, years_to_revenue_domestic)
pv_international_revenue, pv_international_ebitda = calculate_pv_for_business(international_revenue, international_ebitda, discount_rate_international, years_to_revenue_international)
pv_rpm_revenue, pv_rpm_ebitda = calculate_pv_for_business(rpm_revenue, rpm_ebitda, discount_rate_rpm, years_to_revenue_rpm)

# Output the results with proper formatting
st.subheader("Calculated Present Values (PV)")

# Display the results for Domestic, International, and RPM business lines
st.write(f"Domestic Business PV Revenue: ${sum(pv_domestic_revenue.values()):,.0f}")
st.write(f"Domestic Business PV EBITDA: ${sum(pv_domestic_ebitda.values()):,.0f}")

st.write(f"International Business PV Revenue: ${sum(pv_international_revenue.values()):,.0f}")
st.write(f"International Business PV EBITDA: ${sum(pv_international_ebitda.values()):,.0f}")

st.write(f"RPM Business PV Revenue: ${sum(pv_rpm_revenue.values()):,.0f}")
st.write(f"RPM Business PV EBITDA: ${sum(pv_rpm_ebitda.values()):,.0f}")

# Calculate total value using multiples
business_value_domestic_revenue = calculate_business_value(sum(pv_domestic_revenue.values()), revenue_multiple_domestic)
business_value_domestic_ebitda = calculate_business_value(sum(pv_domestic_ebitda.values()), ebit_multiple_domestic)

business_value_international_revenue = calculate_business_value(sum(pv_international_revenue.values()), revenue_multiple_international)
business_value_international_ebitda = calculate_business_value(sum(pv_international_ebitda.values()), ebit_multiple_international)

business_value_rpm_revenue = calculate_business_value(sum(pv_rpm_revenue.values()), revenue_multiple_rpm)
business_value_rpm_ebitda = calculate_business_value(sum(pv_rpm_ebitda.values()), ebit_multiple_rpm)

# Calculate the total business value
total_business_value = business_value_domestic_revenue + business_value_domestic_ebitda + business_value_international_revenue + business_value_international_ebitda + business_value_rpm_revenue + business_value_rpm_ebitda

# Output the total business value
st.write(f"Total Business Value: ${total_business_value:,.0f}")
