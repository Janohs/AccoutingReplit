import streamlit as st
from utils.financial_calculations import (
    generate_trial_balance,
    generate_profit_loss,
    generate_balance_sheet
)
from utils.export_utils import export_to_excel
import os

def render_reports_page(dm):
    st.title("Financial Reports")

    # Get transactions and assets data
    transactions = dm.get_transactions()
    assets = dm.get_assets()

    report_type = st.selectbox(
        "Select Report",
        ["Trial Balance", "Profit and Loss", "Balance Sheet"]
    )

    if report_type == "Trial Balance":
        st.subheader("Trial Balance")
        if not transactions.empty:
            trial_balance = generate_trial_balance(transactions)
            st.dataframe(trial_balance)

            # Show totals
            st.write(f"Total Debit: RM {trial_balance['Debit'].sum():,.2f}")
            st.write(f"Total Credit: RM {trial_balance['Credit'].sum():,.2f}")

            # Export button
            if st.button("Export Trial Balance to Excel"):
                filename = export_to_excel(trial_balance, "trial_balance")
                with open(filename, "rb") as f:
                    st.download_button(
                        label="Download Excel File",
                        data=f,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                os.remove(filename)  # Clean up temporary file
        else:
            st.info("No transactions available for trial balance.")

    elif report_type == "Profit and Loss":
        st.subheader("Profit and Loss Statement")
        if not transactions.empty:
            pl_data = generate_profit_loss(transactions)

            # Income section
            st.write("### Income")
            for category, amount in pl_data['income'].items():
                st.write(f"{category}: RM {amount:,.2f}")
            st.write(f"**Total Income: RM {pl_data['total_income']:,.2f}**")

            # Expenses section
            st.write("### Expenses")
            for category, amount in pl_data['expenses'].items():
                st.write(f"{category}: RM {amount:,.2f}")
            st.write(f"**Total Expenses: RM {pl_data['total_expenses']:,.2f}**")

            # Net Profit
            st.write("### Summary")
            st.write(f"**Net Profit/Loss: RM {pl_data['net_profit']:,.2f}**")

            # Export button
            if st.button("Export Profit & Loss to Excel"):
                filename = export_to_excel(pl_data, "profit_loss")
                with open(filename, "rb") as f:
                    st.download_button(
                        label="Download Excel File",
                        data=f,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                os.remove(filename)  # Clean up temporary file
        else:
            st.info("No transactions available for profit and loss statement.")

    elif report_type == "Balance Sheet":
        st.subheader("Balance Sheet")
        if not transactions.empty:
            bs_data = generate_balance_sheet(transactions, assets)

            # Assets
            st.write("### Assets")
            st.write(f"Current Assets: RM {bs_data['current_assets']:,.2f}")
            st.write(f"Fixed Assets: RM {bs_data['fixed_assets']:,.2f}")
            st.write(f"**Total Assets: RM {bs_data['total_assets']:,.2f}**")

            # Liabilities and Equity
            st.write("### Liabilities and Equity")
            st.write(f"Current Liabilities: RM {bs_data['current_liabilities']:,.2f}")
            st.write(f"Equity: RM {bs_data['equity']:,.2f}")
            st.write(f"**Total Liabilities & Equity: RM {bs_data['total_liabilities_equity']:,.2f}**")

            # Export button
            if st.button("Export Balance Sheet to Excel"):
                filename = export_to_excel(bs_data, "balance_sheet")
                with open(filename, "rb") as f:
                    st.download_button(
                        label="Download Excel File",
                        data=f,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                os.remove(filename)  # Clean up temporary file
        else:
            st.info("No transactions available for balance sheet.")