import pandas as pd
from pathlib import Path

# =========================
# 1. Set file paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output_csv"

OUTPUT_DIR.mkdir(exist_ok=True)

# =========================
# 2. Load required tables
# =========================

customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")
orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")

print("Customers table shape:", customers.shape)
print("Orders table shape:", orders.shape)

# =========================
# 3. Total number of customers
# =========================

# customer_id 是订单层面的用户ID
# customer_unique_id 更接近真实唯一用户
total_customers = customers["customer_id"].nunique()
total_unique_customers = customers["customer_unique_id"].nunique()

total_customer_result = pd.DataFrame({
    "metric": ["total_customer_id", "total_unique_customers"],
    "value": [total_customers, total_unique_customers]
})

total_customer_result.to_csv(
    OUTPUT_DIR / "02_total_customers.csv",
    index=False
)

print("Total customers saved.")

# =========================
# 4. Customer distribution by state
# =========================

customers_by_state = (
    customers
    .groupby("customer_state")
    .size()
    .reset_index(name="customer_count")
    .sort_values(by="customer_count", ascending=False)
)

customers_by_state.to_csv(
    OUTPUT_DIR / "02_customers_by_state.csv",
    index=False
)

print("Customer distribution by state saved.")

# =========================
# 5. Customer distribution by city
# =========================

customers_by_city = (
    customers
    .groupby("customer_city")
    .size()
    .reset_index(name="customer_count")
    .sort_values(by="customer_count", ascending=False)
)

customers_by_city.to_csv(
    OUTPUT_DIR / "02_customers_by_city.csv",
    index=False
)

print("Customer distribution by city saved.")

# =========================
# 6. Orders per customer distribution
# =========================

# orders 表里有 customer_id
# 按 customer_id 统计每个用户下了多少个订单
orders_per_customer = (
    orders
    .groupby("customer_id")
    .size()
    .reset_index(name="order_count")
)

# 再统计：下1单、2单、3单的用户分别有多少
orders_per_customer_distribution = (
    orders_per_customer
    .groupby("order_count")
    .size()
    .reset_index(name="customer_count")
    .sort_values(by="order_count")
)

orders_per_customer.to_csv(
    OUTPUT_DIR / "02_orders_per_customer.csv",
    index=False
)

orders_per_customer_distribution.to_csv(
    OUTPUT_DIR / "02_orders_per_customer_distribution.csv",
    index=False
)

print("Orders per customer distribution saved.")

print("\nCustomer analysis completed successfully.")