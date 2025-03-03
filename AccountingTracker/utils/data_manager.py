import pandas as pd
import os
from datetime import datetime
import shutil

class DataManager:
    def __init__(self):
        self.transactions_file = "data/transactions.csv"
        self.assets_file = "data/assets.csv"
        self._initialize_files()

    def _initialize_files(self):
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/archives", exist_ok=True)

        # Initialize transactions file
        if not os.path.exists(self.transactions_file):
            pd.DataFrame(columns=[
                'date', 'type', 'category', 'description', 'amount', 'payment_method'
            ]).to_csv(self.transactions_file, index=False)

        # Initialize assets file
        if not os.path.exists(self.assets_file):
            pd.DataFrame(columns=[
                'asset_name', 'purchase_date', 'cost', 'useful_life', 'salvage_value'
            ]).to_csv(self.assets_file, index=False)

    def start_new_year(self):
        """Archive current year's data and start fresh"""
        current_year = datetime.now().year
        archive_dir = f"data/archives/{current_year}"
        os.makedirs(archive_dir, exist_ok=True)

        # Archive current files
        if os.path.exists(self.transactions_file):
            shutil.copy2(self.transactions_file, f"{archive_dir}/transactions_{current_year}.csv")
        if os.path.exists(self.assets_file):
            shutil.copy2(self.assets_file, f"{archive_dir}/assets_{current_year}.csv")

        # Create fresh files
        self._initialize_files()

        # Clear current files
        pd.DataFrame(columns=[
            'date', 'type', 'category', 'description', 'amount', 'payment_method'
        ]).to_csv(self.transactions_file, index=False)

        # Keep assets but create a backup
        assets_df = pd.read_csv(self.assets_file)
        assets_df.to_csv(self.assets_file, index=False)

        return current_year

    def add_transaction(self, date, type, category, description, amount, payment_method):
        df = pd.read_csv(self.transactions_file)
        new_transaction = pd.DataFrame([{
            'date': date,
            'type': type,
            'category': category,
            'description': description,
            'amount': amount,
            'payment_method': payment_method
        }])
        df = pd.concat([df, new_transaction], ignore_index=True)
        df.to_csv(self.transactions_file, index=False)

    def delete_transaction(self, index):
        df = pd.read_csv(self.transactions_file)
        df = df.drop(index)
        df.to_csv(self.transactions_file, index=False)

    def get_transactions(self):
        return pd.read_csv(self.transactions_file)

    def get_recent_transactions(self, n=5):
        df = pd.read_csv(self.transactions_file)
        return df.tail(n)

    def get_total_income(self):
        df = pd.read_csv(self.transactions_file)
        return df[df['type'] == 'Income']['amount'].sum()

    def get_total_expenses(self):
        df = pd.read_csv(self.transactions_file)
        return df[df['type'] == 'Expense']['amount'].sum()

    def add_asset(self, asset_name, purchase_date, cost, useful_life, salvage_value):
        df = pd.read_csv(self.assets_file)
        new_asset = pd.DataFrame([{
            'asset_name': asset_name,
            'purchase_date': purchase_date,
            'cost': cost,
            'useful_life': useful_life,
            'salvage_value': salvage_value
        }])
        df = pd.concat([df, new_asset], ignore_index=True)
        df.to_csv(self.assets_file, index=False)

    def get_assets(self):
        return pd.read_csv(self.assets_file)