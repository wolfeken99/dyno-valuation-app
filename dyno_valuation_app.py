import streamlit as st
import pandas as pd
import numpy as np

# Set up title and description
st.title('Implied Business Value Model')
st.write("This model calculates the implied value of a business with three business lines (Domestic, International, RPM), with **FDA approval** as a key input that affects the timeline for each business line.")

# FDA Approval dropdown for each business line
fda_approval_domestic = st.selectbox("FDA Approval - Domestic Business Line", ["Not Approved", "Approved"])
fda_approval_international = st.selectbox("FDA Approval - International Business Line", ["Not Approved", "Approved"])
fda_approval_rpm = st.selectbox("FDA Approval - RPM Business Line", ["Not Approved", "Approved"])

# Discount rates sliders for each business line
discount_rate_ebitda_domestic = st.slider("Discount Rate - Domestic (EBITDA)", min_value=0.0, max_value=1.0, value=0.60, step=0.01)
discount_rate_revenue_domestic = st.slider("Discount Rate - Domestic (Revenue)", min_value=0.0, max_value=1.0, value=0.70, step=0.01)

discount_rate_ebitda_international = st.slider("Discount Rate - International (EBITDA)", min_value=0.0, max_value=1.0, value=0.60, step=0.01)
discount_rate_revenue_international = st.slider("Discount Rate - International (Revenue)", min_value=0.0, max_value=1.0, value=0.70, step=0.01)

discount_rate_ebitda_rpm = st.slider("Discount Rate - RPM (EBITDA)", min_value=0.0, max_value=1.0, value=0.60, step=0.01)
discount_rate_revenue_rpm = st.slider("Discount Rate - RPM (Revenue)", min_value=0.0, max_value=1.0, value=0.70, step=0.01)

# Define the terminal NPV values for each business line
terminal_ebitda_npv_domestic = st.number_input("Terminal (EBITDA) NPV - Domestic", value=110385479.5062)
terminal_revenue_npv_domestic = st.number_input("Terminal (Revenue) NPV - Domestic", value=74505280)

terminal_ebitda_npv_international = st.number_input("Terminal (EBITDA) NPV - International", value=85787179.9469)
terminal_revenue_npv_international = st.number_input("Terminal (Revenue) NPV - International", value=53786956.7871)

terminal_ebitda_npv_rpm = st.number_input("Terminal (EBITDA) NPV - RPM", value=14133345.8229)
terminal_revenue_npv_rpm = st.number_input("Terminal (Revenue) NPV - RPM", value=10676288.3868)

# Define a function to calculate the business line values based on assumptions
def calculate_business_line_value(fda_approval, discount_rate_ebitda, discount_rate_revenue, terminal_ebitda_npv, terminal_revenue_npv):
    # Trigger timeline based on FDA approval
    if fda_approval == "Not Approved":
        timeline_factor = 1.5  # Let's assume it takes 1.5 times longer for Not Approved lines
    else:
        timeline_factor = 1  # Immediate approval for approved lines
    
    # Calculate blended value (could be an average or weighted average depending on the assumptions)
    blended_value = (terminal_ebitda_npv * discount_rate_ebitda + terminal_revenue_npv * discount_rate_revenue) / (discount_rate_ebitda + discount_rate_revenue)
    
    # Adjust blended value based on FDA approval timeline factor
    adjusted_value = blended_value * timeline_factor
    return adjusted_value

# Calculate the blended values for each business line based on the selected parameters
blended_value_domestic = calculate_business_line_value(
    fda_approval_domestic, discount_rate_ebitda_domestic, discount_rate_revenue_domestic, terminal_ebitda_npv_domestic, terminal_revenue_npv_domestic
)

blended_value_international = calculate_business_line_value(
    fda_approval_international, discount_rate_ebitda_international, discount_rate_revenue_international, terminal_ebitda_npv_international, terminal_revenue_npv_international
)

blended_value_rpm = calculate_business_line_value(
    fda_approval_rpm, discount_rate_ebitda_rpm, discount_rate_revenue_rpm, terminal_ebitda_npv_rpm, terminal_revenue_npv_rpm
)

# Summing up the values from all business lines
total_business_value = blended_value_domestic + blended_value_international + blended_value_rpm

# Display the results
st.write(f"### Blended Values for Each Business Line")
st.write(f"Domestic Business Line: ${blended_value_domestic:,.2f}")
st.write(f"International Business Line: ${blended_value_international:,.2f}")
st.write(f"RPM Business Line: ${blended_value_rpm:,.2f}")

st.write(f"### Total Business Value: ${total_business_value:,.2f}")

# Additional outputs (e.g., IRR, MOIC, etc.)
invested_amount = st.number_input("Invested Amount ($)", value=5000000)

# Calculate MOIC (Multiple on Invested Capital) for the total business value
if invested_amount != 0:
    moic = total_business_value / invested_amount
else:
    moic = "N/A"  # In case invested amount is zero

st.write(f"### Investor Return (MOIC Calculation)")
st.write(f"MOIC: {moic}")

