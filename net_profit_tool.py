
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Net Profit per Billable Hour", layout="centered")

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
    st.info("Upload a CSV or check the box to enter data manually.")
    st.info("CSV file must include columns: Revenue, Expenses, Billable Hours.")    
    st.stop()

if billable_hours > 0:
    net_profit = revenue - expenses
    net_profit_per_hour = net_profit / billable_hours
    effective_rate = revenue / billable_hours

    st.subheader("📊 Results")
    st.metric("Net Profit", f"${net_profit:,.2f}")
    st.metric("Net Profit per Billable Hour", f"${net_profit_per_hour:,.2f}")
    st.metric("Effective Hourly Rate (Revenue)", f"${effective_rate:,.2f}")

    # Plot
    fig = px.bar(
        x=["Revenue", "Expenses", "Net Profit"],
        y=[revenue, expenses, net_profit],
        labels={"x": "Metric", "y": "Amount ($)"},
        text_auto=".2s",
        title="Revenue vs Expenses vs Profit"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Billable hours must be greater than 0 to calculate profit per hour.")
