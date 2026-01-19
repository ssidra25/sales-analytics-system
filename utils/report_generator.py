# utils/report_generator.py

from datetime import datetime
from collections import defaultdict
import os


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """

    # -----------------------------
    # SAFETY CHECKS
    # -----------------------------
    if not transactions or not isinstance(transactions, list):
        print("❌ No valid transactions provided to report generator.")
        return

    if not enriched_transactions or not isinstance(enriched_transactions, list):
        print("❌ No valid enriched transactions provided to report generator.")
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # -----------------------------
    # BASIC METRICS
    # -----------------------------
    total_transactions = len(transactions)

    total_revenue = 0
    dates = []

    for tx in transactions:
        try:
            qty = float(tx.get("Quantity", 0))
            price = float(tx.get("UnitPrice", 0))
            total_revenue += qty * price

            if tx.get("Date"):
                dates.append(tx["Date"])
        except Exception:
            continue

    avg_order_value = total_revenue / total_transactions if total_transactions else 0
    start_date = min(dates) if dates else "N/A"
    end_date = max(dates) if dates else "N/A"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -----------------------------
    # REGION-WISE PERFORMANCE
    # -----------------------------
    region_stats = defaultdict(lambda: {"sales": 0, "count": 0})

    for tx in transactions:
        try:
            region = tx.get("Region", "Unknown")
            revenue = float(tx.get("Quantity", 0)) * float(tx.get("UnitPrice", 0))

            region_stats[region]["sales"] += revenue
            region_stats[region]["count"] += 1
        except Exception:
            continue

    sorted_regions = sorted(
        region_stats.items(),
        key=lambda x: x[1]["sales"],
        reverse=True
    )

    # -----------------------------
    # TOP 5 PRODUCTS
    # -----------------------------
    product_stats = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for tx in transactions:
        try:
            name = tx.get("ProductName", "Unknown")
            qty = float(tx.get("Quantity", 0))
            price = float(tx.get("UnitPrice", 0))

            product_stats[name]["qty"] += qty
            product_stats[name]["revenue"] += qty * price
        except Exception:
            continue

    top_products = sorted(
        product_stats.items(),
        key=lambda x: x[1]["revenue"],
        reverse=True
    )[:5]

    # -----------------------------
    # TOP 5 CUSTOMERS
    # -----------------------------
    customer_stats = defaultdict(lambda: {"spent": 0, "orders": 0})

    for tx in transactions:
        try:
            cid = tx.get("CustomerID", "Unknown")
            customer_stats[cid]["spent"] += float(tx.get("Quantity", 0)) * float(tx.get("UnitPrice", 0))
            customer_stats[cid]["orders"] += 1
        except Exception:
            continue

    top_customers = sorted(
        customer_stats.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # -----------------------------
    # DAILY SALES TREND
    # -----------------------------
    daily_stats = defaultdict(lambda: {"revenue": 0, "count": 0, "customers": set()})

    for tx in transactions:
        try:
            date = tx.get("Date", "Unknown")
            daily_stats[date]["revenue"] += float(tx.get("Quantity", 0)) * float(tx.get("UnitPrice", 0))
            daily_stats[date]["count"] += 1
            daily_stats[date]["customers"].add(tx.get("CustomerID", "Unknown"))
        except Exception:
            continue

    # -----------------------------
    # API ENRICHMENT SUMMARY
    # -----------------------------
    enriched_count = 0
    not_enriched_products = set()

    for tx in enriched_transactions:
        if tx.get("API_Match") is True:
            enriched_count += 1
        else:
            not_enriched_products.add(tx.get("ProductName", "Unknown"))

    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    # -----------------------------
    # WRITE REPORT FILE
    # -----------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"         Generated: {now}\n")
        f.write(f"         Records Processed: {total_transactions}\n")
        f.write("=" * 50 + "\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {start_date} to {end_date}\n\n")

        # REGION PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 50 + "\n")
        f.write("Region       Sales           % Total   Transactions\n")
        for region, data in sorted_regions:
            percent = (data["sales"] / total_revenue * 100) if total_revenue else 0
            f.write(f"{region:<12} ₹{data['sales']:>10,.0f}     {percent:>6.2f}%      {data['count']}\n")
        f.write("\n")

        # TOP PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 50 + "\n")
        for i, (name, data) in enumerate(top_products, 1):
            f.write(f"{i}. {name} | Qty: {int(data['qty'])} | Revenue: ₹{data['revenue']:,.2f}\n")
        f.write("\n")

        # TOP CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        for i, (cid, data) in enumerate(top_customers, 1):
            f.write(f"{i}. {cid} | Spent: ₹{data['spent']:,.2f} | Orders: {data['orders']}\n")
        f.write("\n")

        # DAILY TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 50 + "\n")
        for date in sorted(daily_stats.keys()):
            d = daily_stats[date]
            f.write(f"{date} | ₹{d['revenue']:,.2f} | Tx: {d['count']} | Customers: {len(d['customers'])}\n")
        f.write("\n")
# PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 50 + "\n")

        # Best Selling Day
        best_day = None
        best_day_revenue = 0
        best_day_tx = 0

        for date, stats in daily_stats.items():
            if stats["revenue"] > best_day_revenue:
                best_day_revenue = stats["revenue"]
                best_day = date
                best_day_tx = stats["count"]

        f.write("Best Selling Day:\n")
        if best_day:
            f.write(f"{best_day} | Revenue: ₹{best_day_revenue:,.2f} | Transactions: {best_day_tx}\n")
        else:
            f.write("No data available\n")

        f.write("\nLow Performing Products (Qty < 10):\n")

        low_products_found = False
        for product, data in product_stats.items():
            if data["qty"] < 10:
                low_products_found = True
                f.write(
                    f"- {product} | Qty: {int(data['qty'])} | Revenue: ₹{data['revenue']:,.2f}\n"
                )

        if not low_products_found:
            f.write("None\n")

        f.write("\nAverage Transaction Value per Region:\n")
        for region, data in region_stats.items():
            avg_value = data["sales"] / data["count"] if data["count"] else 0
            f.write(
                f"- {region}: ₹{avg_value:,.2f}\n"
            )

        f.write("\n")
        # API SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Products Not Enriched:\n")
        for p in sorted(not_enriched_products):
            f.write(f"- {p}\n")

    print(f"✅ Sales report generated successfully: {output_file}")