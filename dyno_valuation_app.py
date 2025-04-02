 
import streamlit as st
import pandas as pd

# Input values for your business model (adjust as needed)
exit_proceeds = 5000000  # Example exit proceeds
invested_amount = 2000000  # Example invested amount

# Ensure we don't divide by zero
if invested_amount != 0:
    moic = exit_proceeds / invested_amount
else:
    moic = "N/A"  # In case invested amount is zero

# Example data frame for terminal values, EBITDA, revenue, etc.
valuation_results = {
    'Segment': ['Domestic', 'International', 'RPM'],
    'Terminal (EBITDA) NPV': [110385479.5062, 85787179.9469, 14133345.8229],
    'Terminal (Revenue) NPV': [74505280, 53786956.7871, 10676288.3868],
    'Blended Value': [92453739.7531, 69787068.367, 12404817.1048]
}

# Creating a DataFrame for the valuation results
valuation_df = pd.DataFrame(valuation_results)

# Display the valuation results in a table
st.write("Valuation Results")
st.dataframe(valuation_df)

# Investor return calculations
total_pre_money = valuation_df['Blended Value'].sum()
post_money = total_pre_money + 5000000  # Example additional value for post-money valuation
ownership_pct = 5000000 / post_money  # Example ownership percentage
exit_value = valuation_df['Blended Value'].sum()
exit_proceeds = exit_value * ownership_pct

# Display investor return section
st.subheader("Investor Return ($5M Entry)")
st.markdown(f"**Pre-Money Valuation:** ${total_pre_money:,.2f}")
st.markdown(f"**Ownership %:** {ownership_pct*100:.2f}%")
st.markdown(f"**Exit Proceeds:** ${exit_proceeds:,.2f}")
st.markdown(f"**MOIC:** {moic}")

# Displaying IRR calculation if applicable
irr = (exit_proceeds / invested_amount) ** (1 / 5) - 1
st.markdown(f"**IRR:** {irr*100:.1f}%")
