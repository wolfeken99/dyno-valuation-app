import streamlit as st
import pandas as pd

# Define a function to calculate the business line values based on assumptions
def calculate_business_line_value(discount_rate_ebitda, discount_rate_revenue, terminal_ebitda_npv, terminal_revenue_npv):
    # Calculate blended value (could be an average or weighted average depending on the assumptions)
    blended_value = (terminal_ebitda_npv * discount_rate_ebitda + terminal_revenue_npv * discount_rate_revenue) / (discount_rate_ebitda + discount_rate_revenue)
    return blended_value

# Set up title and description
st.title('Implied Business Value Model')
st.write("This model calculates the implied value of a business with three business lines (Domestic, International, RPM).")

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

terminal_ebitda_npv_rpm = st.number_input

