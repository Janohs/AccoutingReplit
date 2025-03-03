import pandas as pd
from datetime import datetime

def calculate_straight_line_depreciation(cost, salvage_value, useful_life):
    """Calculate depreciation using straight-line method"""
    return (cost - salvage_value) / useful_life

def calculate_reducing_balance_depreciation(cost, rate, year):
    """Calculate depreciation using reducing balance method"""
    return cost * (rate/100) * ((1 - rate/100) ** (year - 1))

def calculate_sum_of_years_depreciation(cost, salvage_value, useful_life, current_year):
    """Calculate depreciation using sum of years digits method"""
    sum_of_years = (useful_life * (useful_life + 1)) / 2
    depreciation_factor = (useful_life - current_year + 1) / sum_of_years
    return (cost - salvage_value) * depreciation_factor

def generate_depreciation_schedule(asset, method='straight_line'):
    """Generate complete depreciation schedule for an asset"""
    schedule = []
    cost = asset['cost']
    salvage_value = asset['salvage_value']
    useful_life = asset['useful_life']
    purchase_date = datetime.strptime(asset['purchase_date'], '%Y-%m-%d')

    accumulated_depreciation = 0

    for year in range(1, useful_life + 1):
        if method == 'straight_line':
            annual_depreciation = calculate_straight_line_depreciation(cost, salvage_value, useful_life)
        elif method == 'reducing_balance':
            rate = 20  # Using 20% as default rate
            annual_depreciation = calculate_reducing_balance_depreciation(cost - accumulated_depreciation, rate, year)
        elif method == 'sum_of_years':
            annual_depreciation = calculate_sum_of_years_depreciation(cost, salvage_value, useful_life, year)

        accumulated_depreciation += annual_depreciation
        book_value = cost - accumulated_depreciation

        # Ensure book value doesn't go below salvage value
        if book_value < salvage_value:
            annual_depreciation -= (salvage_value - book_value)
            accumulated_depreciation = cost - salvage_value
            book_value = salvage_value

        schedule.append({
            'year': purchase_date.year + year - 1,
            'annual_depreciation': annual_depreciation,
            'accumulated_depreciation': accumulated_depreciation,
            'book_value': book_value
        })

    return pd.DataFrame(schedule)

def calculate_capital_allowance(assets_df):
    initial_allowance = assets_df['cost'].sum() * 0.20  # 20% initial allowance
    annual_allowance = assets_df['cost'].sum() * 0.10   # 10% annual allowance

    return {
        'initial_allowance': initial_allowance,
        'annual_allowance': annual_allowance,
        'total_allowance': initial_allowance + annual_allowance
    }

def generate_trial_balance(transactions_df):
    debit_accounts = transactions_df[transactions_df['type'] == 'Income'].groupby('category')['amount'].sum()
    credit_accounts = transactions_df[transactions_df['type'] == 'Expense'].groupby('category')['amount'].sum()

    trial_balance = pd.DataFrame({
        'Account': list(debit_accounts.index) + list(credit_accounts.index),
        'Debit': list(debit_accounts.values) + [0] * len(credit_accounts),
        'Credit': [0] * len(debit_accounts) + list(credit_accounts.values)
    })

    return trial_balance

def generate_profit_loss(transactions_df):
    income = transactions_df[transactions_df['type'] == 'Income'].groupby('category')['amount'].sum()
    expenses = transactions_df[transactions_df['type'] == 'Expense'].groupby('category')['amount'].sum()

    total_income = income.sum()
    total_expenses = expenses.sum()
    net_profit = total_income - total_expenses

    return {
        'income': income,
        'expenses': expenses,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit
    }

def generate_balance_sheet(transactions_df, assets_df):
    # Assets
    current_assets = transactions_df[
        (transactions_df['type'] == 'Income') & 
        (transactions_df['payment_method'] == 'Cash')
    ]['amount'].sum()

    fixed_assets = assets_df['cost'].sum()

    # Liabilities
    current_liabilities = transactions_df[
        (transactions_df['type'] == 'Expense') & 
        (transactions_df['payment_method'] == 'Bank')
    ]['amount'].sum()

    # Equity
    equity = current_assets + fixed_assets - current_liabilities

    return {
        'current_assets': current_assets,
        'fixed_assets': fixed_assets,
        'total_assets': current_assets + fixed_assets,
        'current_liabilities': current_liabilities,
        'equity': equity,
        'total_liabilities_equity': current_liabilities + equity
    }