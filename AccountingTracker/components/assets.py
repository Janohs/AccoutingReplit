import streamlit as st
from datetime import datetime
from utils.financial_calculations import (
    generate_depreciation_schedule,
    calculate_capital_allowance
)

def render_assets_page(dm):
    st.title("Assets & Depreciation")

    # Asset Entry Form
    with st.form("asset_form"):
        col1, col2 = st.columns(2)

        with col1:
            asset_name = st.text_input("Asset Name")
            purchase_date = st.date_input("Purchase Date", datetime.now())
            cost = st.number_input("Purchase Cost (RM)", min_value=0.0, format="%.2f")

        with col2:
            useful_life = st.number_input("Useful Life (Years)", min_value=1, value=5)
            salvage_value = st.number_input("Salvage Value (RM)", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Add Asset")

        if submit:
            dm.add_asset(
                asset_name=asset_name,
                purchase_date=purchase_date.strftime("%Y-%m-%d"),
                cost=cost,
                useful_life=useful_life,
                salvage_value=salvage_value
            )
            st.success("Asset added successfully!")

    # Display Assets and Depreciation
    st.subheader("Assets List")
    assets = dm.get_assets()

    if not assets.empty:
        for idx, asset in assets.iterrows():
            with st.expander(f"{asset['asset_name']} - RM {asset['cost']:,.2f}"):
                st.write(f"Purchase Date: {asset['purchase_date']}")
                st.write(f"Useful Life: {asset['useful_life']} years")
                st.write(f"Salvage Value: RM {asset['salvage_value']:,.2f}")

                # Depreciation method selector
                depreciation_method = st.selectbox(
                    "Select Depreciation Method",
                    ["straight_line", "reducing_balance", "sum_of_years"],
                    key=f"dep_method_{idx}"
                )

                # Generate and display depreciation schedule
                schedule = generate_depreciation_schedule(asset, method=depreciation_method)

                # Display schedule in a formatted table
                st.write("### Depreciation Schedule")
                st.dataframe(
                    schedule.style.format({
                        'annual_depreciation': 'RM {:.2f}',
                        'accumulated_depreciation': 'RM {:.2f}',
                        'book_value': 'RM {:.2f}'
                    })
                )

                # Display current year's depreciation
                current_year = datetime.now().year
                current_year_dep = schedule[schedule['year'] == current_year]
                if not current_year_dep.empty:
                    st.write("### Current Year Depreciation")
                    st.metric(
                        "Annual Depreciation",
                        f"RM {current_year_dep.iloc[0]['annual_depreciation']:,.2f}"
                    )
                    st.metric(
                        "Current Book Value",
                        f"RM {current_year_dep.iloc[0]['book_value']:,.2f}"
                    )
    else:
        st.info("No assets recorded yet.")

    # Capital Allowance Section
    st.subheader("Capital Allowance")
    if not assets.empty:
        allowances = calculate_capital_allowance(assets)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Initial Allowance", f"RM {allowances['initial_allowance']:,.2f}")

        with col2:
            st.metric("Annual Allowance", f"RM {allowances['annual_allowance']:,.2f}")

        with col3:
            st.metric("Total Allowance", f"RM {allowances['total_allowance']:,.2f}")
    else:
        st.info("No assets available for capital allowance calculation.")