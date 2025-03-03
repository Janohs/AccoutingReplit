import streamlit as st
from datetime import datetime

def render_expenses_page(dm):
    st.title("Expenses Entry")

    with st.form("expense_form"):
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date", datetime.now())

            # Reorganized expense categories with groups
            expense_categories = {
                "Cost of Goods Sold (COGS)": [
                    "Purchase",
                    "Egg",
                    "Fruits",
                    "Packaging",
                ],
                "Operating Expenses": [
                    "Rental",
                    "Electricity",
                    "Water",
                    "Gas",
                    "Kitchen Supply",
                ],
                "Employee Expenses": [
                    "Staff Salary",
                    "Director's Salary",
                    "Bonus",
                ],
                "Administrative Expenses": [
                    "Stationary",
                    "License and Registration",
                    "Equipment Service",
                ],
                "Other Expenses": [
                    "Upkeep of Shop",
                    "New Equipment",
                    "Others",
                ]
            }

            # Create a flat list of all categories for the selectbox
            all_categories = []
            for group, categories in expense_categories.items():
                all_categories.extend([f"{group} - {cat}" for cat in categories])

            category = st.selectbox(
                "Expense Category",
                all_categories
            )

            payment_method = st.selectbox(
                "Payment Method",
                ["Bank", "Cash"]
            )

        with col2:
            description = st.text_input("Description")
            amount = st.number_input("Amount (RM)", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Add Expense")

        if submit:
            # Extract the actual category without the group prefix
            actual_category = category.split(" - ")[1]

            dm.add_transaction(
                date=date.strftime("%Y-%m-%d"),
                type="Expense",
                category=actual_category,
                description=description,
                amount=amount,
                payment_method=payment_method
            )
            st.success("Expense entry added successfully!")

    # Display expense transactions
    st.subheader("Expense Transactions")
    transactions = dm.get_transactions()
    expense_transactions = transactions[transactions['type'] == 'Expense']

    if not expense_transactions.empty:
        # Group transactions by category groups
        for group, categories in expense_categories.items():
            with st.expander(f"{group} Transactions"):
                group_transactions = expense_transactions[expense_transactions['category'].isin(categories)]
                if not group_transactions.empty:
                    for idx, row in group_transactions.iterrows():
                        st.write(f"**{row['date']} - {row['category']} - RM {row['amount']:,.2f}**")
                        st.write(f"Description: {row['description']}")
                        st.write(f"Payment Method: {row['payment_method']}")
                        if st.button(f"Delete Transaction {idx}", key=f"del_expense_{idx}"):
                            dm.delete_transaction(idx)
                            st.success("Transaction deleted successfully!")
                            st.rerun()
                else:
                    st.info(f"No {group.lower()} recorded yet.")
    else:
        st.info("No expense transactions recorded yet.")