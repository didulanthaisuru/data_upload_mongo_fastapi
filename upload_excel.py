import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from models import Transaction
import uuid

# Load environment variables from .env file
load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["project"]  # Replace with your actual database name
transactions_collection = db["transaction"]

# Excel file path
EXCEL_FILE = "transactions_1.xlsx"  # Ensure the file is in the same directory as this script

def upload_transactions():
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(EXCEL_FILE)

        # Ensure the columns in the DataFrame match the MongoDB collection structure
        df.columns = ["date", "description", "payment", "receipt", "balance"]

        # Convert the "date" column to proper datetime format (DDMONYY -> YYYY-MM-DD)
        df["date"] = pd.to_datetime(df["date"], format='%d%b%y')

        # Replace NaN values in 'description' with an empty string
        df["description"].fillna("", inplace=True)

        # Fill NaN values in payment and receipt columns with 0
        df["payment"].fillna(0.0, inplace=True)
        df["receipt"].fillna(0.0, inplace=True)

        # Remove commas and convert the 'balance', 'payment', and 'receipt' columns to floats
        df["balance"] = df["balance"].replace({',': ''}, regex=True).astype(float)
        df["payment"] = df["payment"].replace({',': ''}, regex=True).astype(float)
        df["receipt"] = df["receipt"].replace({',': ''}, regex=True).astype(float)

        # Convert each row in the DataFrame to a Transaction model and insert into MongoDB
        data = []
        for _, row in df.iterrows():
            # Prepare the row data for MongoDB using the Transaction model
            transaction = Transaction(
                category_id="some_category_id",  # Add your category_id logic here
                account_id="some_account_id",    # Add your account_id logic here
                date=row["date"],
                description=row["description"],
                balance=row["balance"],
                payment=row["payment"],
                receipt=row["receipt"],
                user_id="some_user_id"  # Add your user_id logic here
            ).model_dump()  # Convert to dictionary format suitable for MongoDB insertion
            data.append(transaction)

        # Insert data into MongoDB collection
        transactions_collection.insert_many(data)

        print(f"✅ Successfully uploaded {len(data)} transactions!")
    except Exception as e:
        print(f"❌ Error uploading transactions: {e}")

if __name__ == "__main__":
    upload_transactions()
