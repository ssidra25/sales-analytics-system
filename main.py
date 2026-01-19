
# Clean sales data
from utils.file_handler import clean_sales_data
if __name__ == "__main__":
    df = clean_sales_data("data/sales_data.txt")
    print(df.head())
    print(f"Final shape: {df.shape}")

file_path = "data/sales_data.txt"

#task 1.1
from utils.file_handler import read_sales_data

raw_lines = read_sales_data("data/sales_data.txt")
print("Total lines read:", len(raw_lines))
print(raw_lines[:3])

#task 1.2
from utils.file_handler import read_sales_data
from utils.file_handler import parse_transactions

raw_lines = read_sales_data("data/sales_data.txt")
print("Total records parsed:", len(raw_lines))

clean_data = parse_transactions(raw_lines)

print("First cleaned record:")
print(clean_data[0])

#Task 1.3:
from utils.file_handler import read_sales_data
from utils.file_handler import parse_transactions
from utils.file_handler import validate_and_filter   # ← THIS WAS MISSING / WRONG


def main():
    raw_lines = read_sales_data("data/sales_data.txt")
    print("Total records read:", len(raw_lines))

    clean_data = parse_transactions(raw_lines)
    print("Records after cleaning:", len(clean_data))

    valid_transactions, invalid_count, summary = validate_and_filter(
        clean_data,
        region="North",
        min_amount=1000,
        max_amount=100000
    )

    print("\nValidation Summary:", summary)
    print("Invalid records:", invalid_count)
    print("Final valid transactions:", len(valid_transactions))

    if valid_transactions:
        print("First valid transaction:")
        print(valid_transactions[0])


if __name__ == "__main__":
    main()
    
# Task 2.1(a)
from utils.file_handler import read_sales_data, parse_transactions
from utils.data_processor import calculate_total_revenue

def main():
    # Step 1: Read raw data
    raw_lines = read_sales_data("data/sales_data.txt")

    # Step 2: Parse & clean data
    transactions = parse_transactions(raw_lines)

    # Step 3: Calculate total revenue
    total_revenue = calculate_total_revenue(transactions)

    # Step 4: Display result
    print(f"\nTotal Revenue: {total_revenue:,.2f}")

if __name__ == "__main__":
    main()

# Task 2.1(b):
from utils.file_handler import clean_sales_data
from utils.data_processor import region_wise_sales
import json


def main():
    # Step 1: Clean and load transactions
    transactions = clean_sales_data("data/sales_data.txt")

    # Step 2: Convert DataFrame → list of dicts (tx objects)
    transactions = transactions.to_dict(orient="records")

    # Step 3: Task 2.1(b) – Region-wise sales analysis
    results = region_wise_sales(transactions)

    # Step 4: Display results (pretty format)
    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()

# Task 2.1 (c):
from utils.file_handler import clean_sales_data
from utils.data_processor import top_selling_products
import json

def main():
    # Step 1: Clean and load transactions
    transactions = clean_sales_data("data/sales_data.txt")

    # Step 2: Convert DataFrame → list of dicts (tx objects)
    transactions = transactions.to_dict(orient="records")

    # Step 3: Task 2.1(c) – Top Selling products
    top_products = top_selling_products(transactions, 5)
    print("\nTop Selling Products:")
    for product in top_products:
        print(product)


if __name__ == "__main__":
    main()

# Task 2.1 (d):
from utils.file_handler import clean_sales_data
from utils.data_processor import customer_analysis
import json

def main():
    # Step 1: Clean and load transactions
    transactions = clean_sales_data("data/sales_data.txt")

    # Step 2: Convert DataFrame → list of dicts (tx objects)
    transactions = transactions.to_dict(orient="records")
 # Step 3: Customer analysis
    customer_results = customer_analysis(transactions)

    print("\nCustomer Analysis:")
    for customer_id, stats in customer_results.items():
        print(customer_id, stats)

if __name__ == "__main__":
    main()

#Task 2.2 (a):
from utils.file_handler import clean_sales_data
from utils.data_processor import daily_sales_trend
import json

def main():
    # Step 1: Clean and load transactions
    transactions = clean_sales_data("data/sales_data.txt")

    # Step 2: Convert DataFrame → list of dicts (tx objects)
    transactions = transactions.to_dict(orient="records")
 # Step 3: daily_sales_trend
    daily_results = daily_sales_trend(transactions)
    print("\ndaily sales trend:")
    for date, stats in daily_results.items():
        print(date, stats)
if __name__ == "__main__":
    main()

# Task 2.2(b):
from utils.file_handler import clean_sales_data
from utils.data_processor import find_peak_sales_day
import json

def main():
    # Step 1: Clean and load transactions
    transactions = clean_sales_data("data/sales_data.txt")

    # Step 2: Convert DataFrame → list of dicts (tx objects)
    transactions = transactions.to_dict(orient="records")
 # Step 3: daily_sales_trend
    peak_day= find_peak_sales_day(transactions)
    print("\nPeak Sales Day:")
   
    print(peak_day)
if __name__ == "__main__":
    main()

# Task 2.3:
from utils.file_handler import clean_sales_data
from utils.data_processor import low_performing_products
import json

def main():
    # Step 1: Clean and load transactions
    transactions = clean_sales_data("data/sales_data.txt")

    # Step 2: Convert DataFrame → list of dicts (tx objects)
    transactions = transactions.to_dict(orient="records")
    # step 3:low performing product
    low_products = low_performing_products(transactions, threshold=10)
    print("\nLow Performing Products:")
    for prod in low_products:
     print(prod)
if __name__ == "__main__":
    main()

# Part 3:
from utils.api_handler import (
    get_all_products,
    get_single_product,
    get_products_with_limit,
    search_products
)
import json

def main():
    # 1️⃣ Get ALL products (default 30)
    products, total = get_all_products()
    print("Total products available in API:", total)
    print("Products returned by default:", len(products))

    print("\nFirst product example:")
    print(json.dumps(products[0], indent=2))

    # 2️⃣ Get SINGLE product by ID
    print("\nSingle product (ID = 1):")
    single_product = get_single_product(1)
    print(json.dumps(single_product, indent=2))

    # 3️⃣ Get specific number of products
    limited_products, _ = get_products_with_limit(100)
    print("\nProducts fetched with limit=100:", len(limited_products))

    # 4️⃣ Search products
    search_results, _ = search_products("phone")
    print("\nSearch results for 'phone':", len(search_results))


if __name__ == "__main__":
    main()

# Task 3.1:
# Fetch All Products
from utils.api_handler import fetch_all_products

def main():
    products = fetch_all_products()
    print(products[:3])  # show first 3 products

if __name__ == "__main__":
    main()

# Product Mapping
from utils.api_handler import fetch_all_products, create_product_mapping

def main():
    api_products = fetch_all_products()
    product_map = create_product_mapping(api_products)

    # Print first 3 mappings
    for k in list(product_map.keys())[:3]:
        print(k, ":", product_map[k])

if __name__ == "__main__":
    main()  

# Task 3.2: Enrich_sales_Data
from utils.file_handler import clean_sales_data
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.data_processor import enrich_sales_data, save_enriched_data


def main():
    # Load sales data
    df = clean_sales_data("data/sales_data.txt")
    transactions = df.to_dict(orient="records")

    # Fetch API products
    api_products = fetch_all_products()
    product_mapping = create_product_mapping(api_products)

    # Enrich sales data
    enriched_transactions = enrich_sales_data(transactions, product_mapping)

    # Save enriched data
    save_enriched_data(enriched_transactions)


if __name__ == "__main__":
    main()

# Report generation :
# Task 4.1:
from utils.file_handler import clean_sales_data
from utils.data_processor import (
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    enrich_sales_data
)
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.report_generator import generate_sales_report


def main():
    print("\n🚀 Starting Sales Analytics System...\n")

    # -------------------------------------------------
    # STEP 1: CLEAN SALES DATA
    # -------------------------------------------------
    transactions_df = clean_sales_data("data/sales_data.txt")

    # Convert DataFrame → list of dictionaries
    transactions = transactions_df.to_dict(orient="records")

    print(f"\n✅ Total cleaned transactions: {len(transactions)}")

    # -------------------------------------------------
    # STEP 2: ANALYTICS (TASK 2)
    # -------------------------------------------------
    print("\n📊 Region-wise Sales:")
    region_results = region_wise_sales(transactions)
    for region, stats in region_results.items():
        print(region, stats)

    print("\n📦 Top Selling Products:")
    for product in top_selling_products(transactions):
        print(product)

    print("\n👥 Customer Analysis:")
    customer_results = customer_analysis(transactions)
    for customer, stats in list(customer_results.items())[:5]:
        print(customer, stats)

    print("\n📅 Daily Sales Trend:")
    daily_results = daily_sales_trend(transactions)
    for date, stats in daily_results.items():
        print(date, stats)

    print("\n🔥 Peak Sales Day:")
    print(find_peak_sales_day(transactions))

    print("\n📉 Low Performing Products:")
    for product in low_performing_products(transactions):
        print(product)

    # -------------------------------------------------
    # STEP 3: API INTEGRATION (TASK 3)
    # -------------------------------------------------
    print("\n🌐 Fetching products from DummyJSON API...")
    api_products = fetch_all_products()

    product_mapping = create_product_mapping(api_products)
    print(f"✅ Product mapping created for {len(product_mapping)} products")

    # -------------------------------------------------
    # STEP 3.2: ENRICH SALES DATA
    # -------------------------------------------------
    enriched_transactions = enrich_sales_data(transactions, product_mapping)

    print(f"\n✅ Total enriched transactions: {len(enriched_transactions)}")

    # -------------------------------------------------
    # STEP 4: GENERATE SALES REPORT
    # -------------------------------------------------
    generate_sales_report(
        transactions,
        enriched_transactions,
        output_file="output/sales_report.txt"
    )

    print("\n🎉 Sales Analytics Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()

# Main Application:
# Task 5.1:

from utils.file_handler import clean_sales_data
from utils.data_processor import (
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    enrich_sales_data
)
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.report_generator import generate_sales_report


def main():
    """
    Main execution function
    """

    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # --------------------------------------------------
        # [1/10] Reading & cleaning sales data
        # --------------------------------------------------
        print("\n[1/10] Reading sales data...")
        df = clean_sales_data("data/sales_data.txt")
        transactions = df.to_dict(orient="records")
        print(f"✓ Successfully read {len(transactions)} transactions")

        # --------------------------------------------------
        # [2/10] Parsing & cleaning done
        # --------------------------------------------------
        print("\n[2/10] Parsing and cleaning data...")
        print(f"✓ Parsed {len(transactions)} records")

        # --------------------------------------------------
        # [3/10] Filter options
        # --------------------------------------------------
        regions = sorted(set(tx.get("Region") for tx in transactions))
        amounts = [
            tx["Quantity"] * tx["UnitPrice"]
            for tx in transactions
            if isinstance(tx.get("Quantity"), (int, float))
            and isinstance(tx.get("UnitPrice"), (int, float))
        ]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        if amounts:
            print(f"Amount Range: ₹{int(min(amounts))} - ₹{int(max(amounts))}")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        if choice == "y":
            selected_region = input("Enter region name: ").strip()
            transactions = [
                tx for tx in transactions
                if tx.get("Region") == selected_region
            ]
            print(f"✓ Data filtered for region: {selected_region}")
        else:
            print("✓ No filtering applied")

        # --------------------------------------------------
        # [4/10] Validation summary
        # --------------------------------------------------
        print("\n[4/10] Validating transactions...")
        valid_count = len(transactions)
        print(f"✓ Valid transactions: {valid_count}")

        # --------------------------------------------------
        # [5/10] Analysis (Part 2)
        # --------------------------------------------------
        print("\n[5/10] Analyzing sales data...")
        region_wise_sales(transactions)
        top_selling_products(transactions)
        customer_analysis(transactions)
        daily_sales_trend(transactions)
        find_peak_sales_day(transactions)
        low_performing_products(transactions)
        print("✓ Analysis complete")

        # --------------------------------------------------
        # [6/10] API fetch
        # --------------------------------------------------
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # --------------------------------------------------
        # [7/10] Enrichment
        # --------------------------------------------------
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(transactions, product_mapping)
        print(f"✓ Enriched {len(enriched_transactions)} transactions")

        # --------------------------------------------------
        # [8/10] Saving enriched data
        # --------------------------------------------------
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # --------------------------------------------------
        # [9/10] Generate report
        # --------------------------------------------------
        print("\n[9/10] Generating report...")
        generate_sales_report(
            transactions,
            enriched_transactions,
            output_file="output/sales_report.txt"
        )
        print("✓ Report saved to: output/sales_report.txt")

        # --------------------------------------------------
        # [10/10] Done
        # --------------------------------------------------
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred during execution")
        print("Error:", str(e))
        print("Please check input files and try again.")


if __name__ == "__main__":
    main()