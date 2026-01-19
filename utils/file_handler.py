import pandas as pd
import numpy as np
from pathlib import Path

def clean_sales_data(file_path: str) -> pd.DataFrame:

    with open(file_path, 'r', encoding='latin1', errors='ignore') as file:
        lines = file.readlines()

    header = lines[0]          # keep header
    data_lines = lines[1:]     # skip header
    cleaned_lines = []
    for line in data_lines:
        line = line.strip()
        if not line:
            continue           # skip empty lines
        cleaned_lines.append(line)

    print(f"Total records parsed: {len(cleaned_lines)}")
    # Read raw lines (handles non-UTF8 automatically)
    with open(file_path, 'r', encoding='latin1', errors='ignore') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    total_parsed = len(lines)
    data = []
    
    for line in lines:
        try:
            # Split by pipe, handle variable field counts
            fields = line.split('|')
            if len(fields) < 8:
                continue
                
            # Extract and clean fields
            transaction_id = fields[0].strip()
            date = fields[1].strip()
            product_id = fields[2].strip()
            product_name = fields[3].strip().replace(',', '')  # Clean product name
            quantity_str = fields[4].strip().replace(',', '')
            unit_price_str = fields[5].strip().replace(',', '')
            customer_id = fields[6].strip()
            region = fields[7].strip()
            
            # Convert numerics
            quantity = pd.to_numeric(quantity_str, errors='coerce')
            unit_price = pd.to_numeric(unit_price_str, errors='coerce')
            
            # Only process if basic parsing worked
            if pd.isna(quantity) or pd.isna(unit_price):
                continue
                
            data.append({
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            })
            
        except:
            continue
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Apply business rules to filter invalid records
    invalid_mask = (
        df['CustomerID'].isna() | (df['CustomerID'] == '') |
        df['Region'].isna() | (df['Region'] == '') |
        (df['Quantity'] <= 0) |
        (df['UnitPrice'] <= 0) |
        (~df['TransactionID'].str.startswith('T'))
    )
    
    invalid_count = invalid_mask.sum()
    valid_df = df[~invalid_mask].copy()
    
    # REQUIRED OUTPUT
  
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_df)}")
    
    return valid_df

#Task 1.1:
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns a list of raw transaction lines (strings).
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()

            # Remove header and empty lines
            cleaned_lines = []
            for line in lines[1:]:  # skip header
                line = line.strip()
                if line:
                    cleaned_lines.append(line)

            return cleaned_lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []

#Task 1.2:
def parse_transactions(raw_lines):
    """
    Parses raw sales lines into cleaned transaction dictionaries.
    Returns a list of dictionaries.
    """

    cleaned_data = []
    invalid_count = 0

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            invalid_count += 1
            continue

        try:
            transaction_id = parts[0].strip()
            date = parts[1].strip()
            product_id = parts[2].strip()

            # Clean ProductName (remove commas)
            product_name = parts[3].replace(",", "").strip()

            # Clean Quantity
            quantity = int(parts[4].replace(",", "").strip())

            # Clean UnitPrice
            unit_price = float(parts[5].replace(",", "").strip())

            customer_id = parts[6].strip()
            region = parts[7].strip()

            # Basic validation rules
            if (
                not transaction_id.startswith("T")
                or quantity <= 0
                or unit_price <= 0
                or customer_id == ""
                or region == ""
            ):
                invalid_count += 1
                continue

            cleaned_data.append({
                "TransactionID": transaction_id,
                "Date": date,
                "ProductID": product_id,
                "ProductName": product_name,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "CustomerID": customer_id,
                "Region": region
            })

        except ValueError:
            invalid_count += 1
            continue

    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(cleaned_data)}")

    return cleaned_data
#Task 1.3:
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    # Summary counters
    total_input = len(transactions)
    filtered_by_region = 0
    filtered_by_amount = 0

    # Show available regions
    regions = sorted(set(tx.get("Region") for tx in transactions if tx.get("Region")))
    print("Available regions:", regions)

    # Show transaction amount range
    amounts = [
        tx["Quantity"] * tx["UnitPrice"]
        for tx in transactions
        if isinstance(tx.get("Quantity"), int) and isinstance(tx.get("UnitPrice"), (int, float))
    ]

    if amounts:
        print("Transaction amount range:", min(amounts), "to", max(amounts))

    for tx in transactions:
        try:
            # ---------- VALIDATION ----------
            if (
                tx["Quantity"] <= 0
                or tx["UnitPrice"] <= 0
                or not tx["TransactionID"].startswith("T")
                or not tx["ProductID"].startswith("P")
                or not tx["CustomerID"].startswith("C")
            ):
                invalid_count += 1
                continue

            amount = tx["Quantity"] * tx["UnitPrice"]

            # ---------- FILTER BY REGION ----------
            if region and tx["Region"] != region:
                filtered_by_region += 1
                continue

            # ---------- FILTER BY AMOUNT ----------
            if min_amount and amount < min_amount:
                filtered_by_amount += 1
                continue

            if max_amount and amount > max_amount:
                filtered_by_amount += 1
                continue

            valid_transactions.append(tx)

        except KeyError:
            invalid_count += 1

    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions),
    }

    return valid_transactions, invalid_count, filter_summary

