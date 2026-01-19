# Task 2.1 
#Task 2.1(a):
# utils/data_processor.py
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Each transaction is expected to be a dictionary or object 
    containing 'Quantity' and 'UnitPrice'.
    """
    total_revenue = 0.0
    
    for item in transactions:
        # Multiply quantity by price and add to the running total
        total_revenue += item['Quantity'] * item['UnitPrice']
        
    return float(total_revenue)

# Example Usage:
# sample_data = [
#     {'Quantity': 10, 'UnitPrice': 100.0},
#     {'Quantity': 5, 'UnitPrice': 200.0}
# ]
# print(calculate_total_revenue(sample_data)) # Output: 2000.0

# Task 2.1 (b):
def region_wise_sales(transactions):
    result = {}

    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"]*tx["UnitPrice"]

        if region not in result:
            result[region] = {
                "total_sales": 0,
                "transaction_count": 0
            }

        result[region]["total_sales"] += amount
        result[region]["transaction_count"] += 1

    return result

# Task 2.1 (c):
def top_selling_products(transactions, n=5):
    product_summary = {}

    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_summary:
            product_summary[product] = {
                "total_quantity": 0,
                "total_revenue": 0
            }

        product_summary[product]["total_quantity"] += quantity
        product_summary[product]["total_revenue"] += revenue

    # Convert to required output format
    result = [
        (product,
         data["total_quantity"],
         round(data["total_revenue"], 2))
        for product, data in product_summary.items()
    ]

    # Sort by total quantity (descending)
    result.sort(key=lambda x: x[1], reverse=True)

    # Return top n products
    return result[:n]

# Task 2.1 (d):
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """

    customer_stats = {}

    for tx in transactions:
        customer_id = tx["CustomerID"]
        product_name = tx["ProductName"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if customer_id not in customer_stats:
            customer_stats[customer_id] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_stats[customer_id]["total_spent"] += amount
        customer_stats[customer_id]["purchase_count"] += 1
        customer_stats[customer_id]["products_bought"].add(product_name)

    # Final formatting
    for customer_id, stats in customer_stats.items():
        stats["avg_order_value"] = round(
            stats["total_spent"] / stats["purchase_count"], 2
        )
        stats["products_bought"] = list(stats["products_bought"])

    # Sort by total_spent descending
    sorted_customers = dict(
        sorted(
            customer_stats.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers

# Task 2.2 (a):
from collections import defaultdict

def daily_sales_trend(transactions):
    daily_data = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0,
        'customers': set()
    })

    # Step 1: Aggregate data by date
    for tx in transactions:
        date = tx['Date']
        revenue = tx['Quantity'] * tx['UnitPrice']
        customer_id = tx['CustomerID']

        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer_id)

    # Step 2: Convert customer sets to counts
    result = {}
    for date, values in daily_data.items():
        result[date] = {
            'revenue': round(values['revenue'], 2),
            'transaction_count': values['transaction_count'],
            'unique_customers': len(values['customers'])
        }

    # Step 3: Sort by date (chronological order)
    sorted_result = dict(sorted(result.items()))

    return sorted_result

# Task 2.2(b):
from collections import defaultdict

def find_peak_sales_day(transactions):
    daily_revenue = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0
    })

    # Step 1: Aggregate revenue per day
    for tx in transactions:
        date = tx['Date']
        revenue = tx['Quantity'] * tx['UnitPrice']

        daily_revenue[date]['revenue'] += revenue
        daily_revenue[date]['transaction_count'] += 1

    # Step 2: Find peak sales day
    peak_date = None
    peak_revenue = 0.0
    peak_transactions = 0

    for date, stats in daily_revenue.items():
        if stats['revenue'] > peak_revenue:
            peak_revenue = stats['revenue']
            peak_transactions = stats['transaction_count']
            peak_date = date

    return (peak_date, round(peak_revenue, 2), peak_transactions)

# Task 2.3(a):
def low_performing_products(transactions, threshold=10):
    product_summary = {}

    # Step 1: Aggregate quantity and revenue by product
    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_summary:
            product_summary[product] = {
                "total_quantity": 0,
                "total_revenue": 0
            }

        product_summary[product]["total_quantity"] += quantity
        product_summary[product]["total_revenue"] += revenue

    # Step 2: Filter products below threshold
    low_products = [
        (product, data["total_quantity"], round(data["total_revenue"], 2))
        for product, data in product_summary.items()
        if data["total_quantity"] < threshold
    ]

    # Step 3: Sort by total_quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products

# Task 3.2:Enrich_sales_Data
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        try:
            # Extract numeric product ID (P101 -> 101)
            product_id_str = tx.get("ProductID", "")
            numeric_id = int("".join(filter(str.isdigit, product_id_str)))

            if numeric_id in product_mapping:
                api_product = product_mapping[numeric_id]

                enriched_tx["API_Category"] = api_product.get("category")
                enriched_tx["API_Brand"] = api_product.get("brand")
                enriched_tx["API_Rating"] = api_product.get("rating")
                enriched_tx["API_Match"] = True
            else:
                enriched_tx["API_Category"] = None
                enriched_tx["API_Brand"] = None
                enriched_tx["API_Rating"] = None
                enriched_tx["API_Match"] = False

        except Exception:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched_transactions.append(enriched_tx)

    print(f"Total records enriched: {len(enriched_transactions)}")

    return enriched_transactions
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    if not enriched_transactions:
        print("⚠️ No enriched data to save.")
        return

    headers = list(enriched_transactions[0].keys())

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = []
            for col in headers:
                value = tx.get(col)
                row.append("" if value is None else str(value))
            file.write("|".join(row) + "\n")

    print(f"✅ Enriched data saved to {filename}")
    print(f"Total records written: {len(enriched_transactions)}")