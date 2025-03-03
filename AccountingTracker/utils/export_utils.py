import pandas as pd
from datetime import datetime

def export_to_excel(data, report_type):
    """
    Export data to Excel file with proper formatting
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report_type}_{timestamp}.xlsx"
    
    # Create Excel writer object
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    
    if report_type == "trial_balance":
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Trial Balance', index=False)
        
    elif report_type == "profit_loss":
        # Income section
        income_df = pd.DataFrame({
            'Category': data['income'].index,
            'Amount (RM)': data['income'].values
        })
        income_df.to_excel(writer, sheet_name='Profit & Loss', startrow=1, index=False)
        
        # Expenses section
        expenses_df = pd.DataFrame({
            'Category': data['expenses'].index,
            'Amount (RM)': data['expenses'].values
        })
        expenses_df.to_excel(writer, sheet_name='Profit & Loss', startrow=len(income_df)+4, index=False)
        
        # Summary
        summary_df = pd.DataFrame({
            'Item': ['Total Income', 'Total Expenses', 'Net Profit/Loss'],
            'Amount (RM)': [data['total_income'], data['total_expenses'], data['net_profit']]
        })
        summary_df.to_excel(writer, sheet_name='Profit & Loss', startrow=len(income_df)+len(expenses_df)+7, index=False)
        
    elif report_type == "balance_sheet":
        # Assets section
        assets_df = pd.DataFrame({
            'Item': ['Current Assets', 'Fixed Assets', 'Total Assets'],
            'Amount (RM)': [data['current_assets'], data['fixed_assets'], data['total_assets']]
        })
        assets_df.to_excel(writer, sheet_name='Balance Sheet', startrow=1, index=False)
        
        # Liabilities and Equity section
        liab_equity_df = pd.DataFrame({
            'Item': ['Current Liabilities', 'Equity', 'Total Liabilities & Equity'],
            'Amount (RM)': [data['current_liabilities'], data['equity'], data['total_liabilities_equity']]
        })
        liab_equity_df.to_excel(writer, sheet_name='Balance Sheet', startrow=len(assets_df)+4, index=False)
    
    writer.close()
    return filename
