import streamlit as st
from datetime import datetime

def render_income_page(dm):
    st.title("Income Entry")

    with st.form("income_form"):
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date", datetime.now())
            category = st.selectbox(
                "Income Category",
                ["Bank Sale", "Cash Sale"]
            )

        with col2:
            description = st.text_input("Description")
            amount = st.number_input("Amount (RM)", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Add Income")

        if submit:
            dm.add_transaction(
                date=date.strftime("%Y-%m-%d"),
                type="Income",
                category=category,
                description=description,
                amount=amount,
                payment_method="Bank" if category == "Bank Sale" else "Cash"
            )
            st.success("Income entry added successfully!")

    # Display income transactions
    st.subheader("Income Transactions")
    transactions = dm.get_transactions()
    income_transactions = transactions[transactions['type'] == 'Income']

    if not income_transactions.empty:
        for idx, row in income_transactions.iterrows():
            with st.expander(f"{row['date']} - {row['category']} - RM {row['amount']:,.2f}"):
                st.write(f"Description: {row['description']}")
                st.write(f"Payment Method: {row['payment_method']}")
                if st.button(f"Delete Transaction {idx}", key=f"del_income_{idx}"):
                    dm.delete_transaction(idx)
                    st.success("Transaction deleted successfully!")
                    st.rerun()
    else:
        st.info("No income transactions recorded yet.")