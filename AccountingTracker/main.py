import streamlit as st
import pandas as pd
from datetime import datetime
from components import income, expenses, reports, assets
from utils import data_manager, financial_calculations

st.set_page_config(
    page_title="RM Accounting System",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .reportBlock {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("RM Accounting System")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Income", "Expenses", "Reports", "Assets & Depreciation"]
)

# Initialize data manager
dm = data_manager.DataManager()

# Page routing
if page == "Dashboard":
    st.title("Financial Dashboard")

    # New Year Button
    if st.button("Start New Accounting Year"):
        if st.session_state.get('confirm_new_year', False):
            archived_year = dm.start_new_year()
            st.success(f"Previous year's data has been archived to data/archives/{archived_year}. New year started successfully!")
            st.session_state.confirm_new_year = False
            st.rerun()
        else:
            st.warning("⚠️ Are you sure you want to start a new accounting year? This will archive current data and create fresh files.")
            st.session_state.confirm_new_year = True
            st.button("Yes, I'm sure", key="confirm_button")

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        total_income = dm.get_total_income()
        st.metric("Total Income", f"RM {total_income:,.2f}")

    with col2:
        total_expenses = dm.get_total_expenses()
        st.metric("Total Expenses", f"RM {total_expenses:,.2f}")

    with col3:
        net_profit = total_income - total_expenses
        st.metric("Net Profit", f"RM {net_profit:,.2f}")

    # Recent transactions
    st.subheader("Recent Transactions")
    recent_trans = dm.get_recent_transactions(5)
    st.table(recent_trans)

elif page == "Income":
    income.render_income_page(dm)

elif page == "Expenses":
    expenses.render_expenses_page(dm)

elif page == "Reports":
    reports.render_reports_page(dm)

elif page == "Assets & Depreciation":
    assets.render_assets_page(dm)