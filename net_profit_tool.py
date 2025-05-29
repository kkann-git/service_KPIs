
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Net Profit per Billable Hour", layout="wide")

st.title("💰 Net Profit per Billable Hour Calculator")

st.markdown("Use this tool to calculate your true profitability based on your time and expenses.")

# Input method
upload = st.file_uploader("Upload a CSV file with your financial data", type="csv")
manual = st.checkbox("Or enter data manually")

if upload:
    df = pd.read_csv(upload)
    st.write("Preview of uploaded data:")
    st.dataframe(df)

    try:
        revenue = df["Revenue"].sum()
        expenses = df["Expenses"].sum()
        billable_hours = df["Billable Hours"].sum()
    except KeyError:
        st.error("CSV must include columns: Revenue, Expenses, Billable Hours")
        st.stop()

elif manual:
    revenue = st.number_input("Total Revenue", min_value=0.0, step=100.0)
    expenses = st.number_input("Total Expenses", min_value=0.0, step=100.0)
    billable_hours = st.number_input("Total Billable Hours", min_value=0.0, step=1.0)
else:
    st.info("Upload a CSV or check the box to enter data manually. CSV file must include columns: Revenue, Expenses, Billable Hours.")
    st.info("Entered data will only be stored in memory (RAM) only for the duration of the session and is deleted as soon as it is no longer needed—such as when the user uploads another file, clears the file uploader, or closes the browser tab. This data is not saved to disk or permanently stored in this app.")    
    st.stop()

if billable_hours > 0:
    net_profit = revenue - expenses
    net_profit_per_hour = net_profit / billable_hours
    effective_rate = revenue / billable_hours

    col1, col2, col3 = st.columns([1,3,2])

    col1.subheader("📊 Results")
    col1.metric("Net Profit", f"${net_profit:,.2f}")
    col1.metric("Net Profit per Billable Hour", f"${net_profit_per_hour:,.2f}")
    col1.metric("Effective Hourly Rate (Revenue)", f"${effective_rate:,.2f}")

    # Plot
    fig = px.bar(
        x=["Revenue", "Expenses", "Net Profit"],
        y=[revenue, expenses, net_profit],
        labels={"x": "Metric", "y": "Amount ($)"},
        text_auto=".2s",
        title="Revenue vs Expenses vs Profit"
    )
    col2.plotly_chart(fig, use_container_width=True)    

    # Reference Data Table
    col3.markdown("While industry-specific data can vary, here are some general reference points from consulting, agency, and trade business benchmarks.")
    
    ref_data = {'Industry': ['Freelance/Consulting', 'Marketing/Creative Agencies', 'Trades (Plumbing, HVAC)', 'Coaches/Consultants'], 
                'Target Net Profit per Billable Hour': ['$75 – $150/hr', '$60 – $120/hr', '$50 – $100/hr', '$80 – $200/hr']}
    df_ref = pd.DataFrame(ref_data)
    col3.table(df_ref.style.hide_index())
else:
    st.warning("Billable hours must be greater than 0 to calculate profit per hour.")
