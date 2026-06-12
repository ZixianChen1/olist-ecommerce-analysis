import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================
# 1. Set file paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output_csv"
FIGURE_DIR = BASE_DIR / "figures"

FIGURE_DIR.mkdir(exist_ok=True)

# =========================
# 2. Load prepared CSV results
# =========================

order_status = pd.read_csv(OUTPUT_DIR / "03_order_status_distribution.csv")
monthly_orders = pd.read_csv(OUTPUT_DIR / "03_monthly_order_count.csv")
category_sales = pd.read_csv(OUTPUT_DIR / "04_category_sales_count.csv")
customers_by_state = pd.read_csv(OUTPUT_DIR / "02_customers_by_state.csv")

# =========================
# 3. Order status pie chart
# =========================

# Combine small status categories into "others"
order_status_pie = order_status.copy()

main_status = order_status_pie[order_status_pie["order_ratio"] >= 0.01]
small_status = order_status_pie[order_status_pie["order_ratio"] < 0.01]

if len(small_status) > 0:
    others_row = pd.DataFrame({
        "order_status": ["others"],
        "order_count": [small_status["order_count"].sum()],
        "order_ratio": [small_status["order_ratio"].sum()]
    })

    order_status_pie = pd.concat([main_status, others_row], ignore_index=True)
else:
    order_status_pie = main_status

plt.figure(figsize=(9, 7))

wedges, texts, autotexts = plt.pie(
    order_status_pie["order_count"],
    labels=None,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.75
)

plt.title("Order Status Distribution")

plt.legend(
    wedges,
    order_status_pie["order_status"],
    title="Order Status",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

plt.tight_layout()
plt.savefig(FIGURE_DIR / "01_order_status_pie.png", dpi=300, bbox_inches="tight")
plt.close()

print("Order status pie chart saved.")

# =========================
# 4. Monthly order count line chart
# =========================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_orders["order_month"],
    monthly_orders["order_count"],
    marker="o"
)

plt.title("Monthly Order Count")
plt.xlabel("Month")
plt.ylabel("Order Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIGURE_DIR / "02_monthly_order_count_line.png", dpi=300)
plt.close()

print("Monthly order count line chart saved.")

# =========================
# 5. Top 10 category sales bar chart
# =========================

top10_category_sales = category_sales.head(10)

plt.figure(figsize=(12, 6))

plt.bar(
    top10_category_sales["product_category_name"],
    top10_category_sales["sales_count"]
)

plt.title("Top 10 Categories by Sales Count")
plt.xlabel("Product Category")
plt.ylabel("Sales Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(FIGURE_DIR / "03_top10_category_sales_bar.png", dpi=300)
plt.close()

print("Top 10 category sales bar chart saved.")

# =========================
# 6. Customer distribution by state bar chart
# =========================

plt.figure(figsize=(12, 6))

plt.bar(
    customers_by_state["customer_state"],
    customers_by_state["customer_count"]
)

plt.title("Customer Distribution by State")
plt.xlabel("Customer State")
plt.ylabel("Customer Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIGURE_DIR / "04_customer_state_distribution_bar.png", dpi=300)
plt.close()

print("Customer state distribution bar chart saved.")

print("\nVisualization completed successfully.")