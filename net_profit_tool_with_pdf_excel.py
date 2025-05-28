
import streamlit as st
import pandas as pd
import plotly.express as px
import pdfkit
import tempfile
import os

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

    # PDF Export
    st.subheader("📄 Export Report")

    html_content = f"""
    <h2>Net Profit Report</h2>
    <p><strong>Total Revenue:</strong> ${revenue:,.2f}</p>
    <p><strong>Total Expenses:</strong> ${expenses:,.2f}</p>
    <p><strong>Net Profit:</strong> ${net_profit:,.2f}</p>
    <p><strong>Billable Hours:</strong> {billable_hours}</p>
    <p><strong>Net Profit per Billable Hour:</strong> ${net_profit_per_hour:,.2f}</p>
    <p><strong>Effective Hourly Rate (Revenue):</strong> ${effective_rate:,.2f}</p>
    """

    if st.button("Generate PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
            tmp_html.write(html_content.encode("utf-8"))
            tmp_html_path = tmp_html.name

        pdf_path = tmp_html_path.replace(".html", ".pdf")
        pdfkit.from_file(tmp_html_path, pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download PDF Report",
                data=f,
                file_name="net_profit_report.pdf",
                mime="application/pdf"
            )

        os.remove(tmp_html_path)
        os.remove(pdf_path)
else:
    st.warning("Billable hours must be greater than 0 to calculate profit per hour.")


    # Excel Export
    st.subheader("📊 Export to Excel")

    export_data = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Expenses",
            "Net Profit",
            "Billable Hours",
            "Net Profit per Billable Hour",
            "Effective Hourly Rate (Revenue)"
        ],
        "Value": [
            revenue,
            expenses,
            net_profit,
            billable_hours,
            net_profit_per_hour,
            effective_rate
        ]
    })

    excel_file_path = os.path.join(tempfile.gettempdir(), "net_profit_report.xlsx")
    export_data.to_excel(excel_file_path, index=False)

    with open(excel_file_path, "rb") as f:
        st.download_button(
            label="📥 Download Excel Report",
            data=f,
            file_name="net_profit_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
