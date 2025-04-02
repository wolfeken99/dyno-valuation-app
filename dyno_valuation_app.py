import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Set up title and description
st.title('Implied Business Value Model')
st.write("""
    This model calculates the implied value of a business with three business lines: 
    Domestic Hospital, International Hospital, and RPM. The revenue for each business 
    line is triggered by FDA approval, which is set to occur on **December 31, 2025**. 
    Each business line has a different lag before revenue generation begins.
""")

# FDA Approval Date input (default is December 31, 2025)
fda_approval_date = st.date_input("FDA Approval Date", datetime(2025, 12, 31))

# Define revenue start delays for each business line (in months)
revenue_delay_domestic = 6  # Domestic takes 6 months after FDA approval to start generating revenue
revenue_delay_international_rpm = 12  # International and RPM take 12 months

# Discount rates sliders for each business line (ranging from 0 to 1)
discount_rate_ebitda_domestic = st.slider("Discount Rate - Domestic (EBITDA)", min_value=0.0, max_value=1.0, value=0.60, step=0.01)
discount_rate_revenue_domestic = st.slider("Discount Rate - Domestic (Revenue)", min_value=0.0, max_value=1.0, value=0.70, step=0.01)

discount_rate_ebitda_international = st.slider("Discount Rate - International (EBITDA)", min_value=0.0, max_value=1.0, value=0.60, step=0.01)
discount_rate_revenue_international = st.slider("Discount Rate - International (Revenue)", min_value=0.0, max_value=1.0, value=0.70, step=0.01)

discount_rate_ebitda_rpm = st.slider("Discount Rate - RPM (EBITDA)", min_value=0.0, max_value=1.0, value=0.60, step=0.01)
discount_rate_revenue_rpm = st.slider("Discount Rate - RPM (Revenue)", min_value=0.0, max_value=1.0, value=0.70, step=0.01)

# Define the terminal NPV values for each business line (for simplicity, assume fixed values)
terminal_ebitda_npv_domestic = st.number_input("Terminal (EBITDA) NPV - Domestic", value=1103854795062.0)
terminal_revenue_npv_domestic = st.number_input("Terminal (Revenue) NPV - Domestic", value=74505280.0)

terminal_ebitda_npv_international = st.number_input("Terminal (EBITDA) NPV - International", value=857871799469.0)
terminal_revenue_npv_international = st.number_input("Terminal (Revenue) NPV - International", value=537869567871.0)

terminal_ebitda_npv_rpm = st.number_input("Terminal (EBITDA) NPV - RPM", value=141333458229.0)
terminal_revenue_npv_rpm = st.number_input("Terminal (Revenue) NPV - RPM", value=106762883868.0)

# Define a function to calculate the business line values based on assumptions and FDA approval
def calculate_business_line_value(fda_approval_date, revenue_delay_months, discount_rate_ebitda, discount_rate_revenue, terminal_ebitda_npv, terminal_revenue_npv):
    # Calculate the revenue start date based on FDA approval and the delay for each business line
    revenue_start_date = fda_approval_date + timedelta(days=revenue_delay_months * 30)  # 30 days per month
    today = datetime.today().date()

    # Check if the business line has started generating revenue
    if today >= revenue_start_date:
        revenue_start = True
    else:
        revenue_start = False

    # If the business line has started generating revenue, calculate the blended value
    if revenue_start:
        blended_value = (terminal_ebitda_npv * discount_rate_ebitda + terminal_revenue_npv * discount_rate_revenue) / (discount_rate_ebitda + discount_rate_revenue)
    else:
        blended_value = 0  # If revenue hasn't started yet, the value is 0

    return blended_value

# Calculate the blended values for each business line based on the selected parameters
blended_value_domestic = calculate_business_line_value(
    fda_approval_date, revenue_delay_domestic, discount_rate_ebitda_domestic, discount_rate_revenue_domestic, terminal_ebitda_npv_domestic, terminal_revenue_npv_domestic
)

blended_value_international = calculate_business_line_value(
    fda_approval_date, revenue_delay_international_rpm, discount_rate_ebitda_international, discount_rate_revenue_international, terminal_ebitda_npv_international, terminal_revenue_npv_international
)

blended_value_rpm = calculate_business_line_value(
    fda_approval_date, revenue_delay_international_rpm, discount_rate_ebitda_rpm, discount_rate_revenue_rpm, terminal_ebitda_npv_rpm, terminal_revenue_npv_rpm
)

# Summing up the values from all business lines
total_business_value = blended_value_domestic + blended_value_international + blended_value_rpm

# Display the results
st.write(f"### Blended Values for Each Business Line")
st.write(f"Domestic Business Line: ${blended_value_domestic:,.0f}")
st.write(f"International Business Line: ${blended_value_international:,.0f}")
st.write(f"RPM Business Line: ${blended_value_rpm:,.0f}")

st.write(f"### Total Business Value: ${total_business_value:,.0f}")

# Additional outputs (e.g., IRR, MOIC, etc.)
invested_amount = st.number_input("Invested Amount ($)", value=5000000)

# Calculate MOIC (Multiple on Invested Capital) for the total business value
if invested_amount != 0:
    moic = total_business_value / invested_amount
else:
    moic = "N/A"  # In case invested amount is zero

st.write(f"### Investor Return (MOIC Calculation)")
st.write(f"MOIC: {moic}")
