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

orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")

print("Orders table shape:", orders.shape)
print("Order items table shape:", order_items.shape)

# =========================
# 3. Total number of orders
# =========================

total_orders = orders["order_id"].nunique()

total_orders_result = pd.DataFrame({
    "metric": ["total_orders"],
    "value": [total_orders]
})

total_orders_result.to_csv(
    OUTPUT_DIR / "03_total_orders.csv",
    index=False
)

print("Total orders saved.")

# =========================
# 4. Order status distribution
# =========================

order_status_distribution = (
    orders["order_status"]
    .value_counts()
    .reset_index()
)

order_status_distribution.columns = ["order_status", "order_count"]

order_status_distribution["order_ratio"] = (
    order_status_distribution["order_count"] / total_orders
)

order_status_distribution.to_csv(
    OUTPUT_DIR / "03_order_status_distribution.csv",
    index=False
)

print("Order status distribution saved.")

# =========================
# 5. Convert order purchase time to datetime
# =========================

# order_purchase_timestamp 是订单购买时间
# 先把它从字符串转换成 datetime 类型，后面才能按天、周、月统计
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# =========================
# 6. Daily order count
# =========================

orders["order_date"] = orders["order_purchase_timestamp"].dt.date

daily_order_count = (
    orders
    .groupby("order_date")
    .size()
    .reset_index(name="order_count")
    .sort_values(by="order_date")
)

daily_order_count.to_csv(
    OUTPUT_DIR / "03_daily_order_count.csv",
    index=False
)

print("Daily order count saved.")

# =========================
# 7. Weekly order count
# =========================

orders["order_week"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("W")
    .astype(str)
)

weekly_order_count = (
    orders
    .groupby("order_week")
    .size()
    .reset_index(name="order_count")
    .sort_values(by="order_week")
)

weekly_order_count.to_csv(
    OUTPUT_DIR / "03_weekly_order_count.csv",
    index=False
)

print("Weekly order count saved.")

# =========================
# 8. Monthly order count
# =========================

orders["order_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

monthly_order_count = (
    orders
    .groupby("order_month")
    .size()
    .reset_index(name="order_count")
    .sort_values(by="order_month")
)

monthly_order_count.to_csv(
    OUTPUT_DIR / "03_monthly_order_count.csv",
    index=False
)

print("Monthly order count saved.")

# =========================
# 9. Order amount distribution
# =========================

# order_items 表中每一行是一件订单商品
# price 是商品价格
# freight_value 是运费
# 这里先按 order_id 汇总每个订单的商品金额和运费
order_amount = (
    order_items
    .groupby("order_id")
    .agg(
        total_product_amount=("price", "sum"),
        total_freight_amount=("freight_value", "sum")
    )
    .reset_index()
)

# 总订单金额 = 商品金额 + 运费
order_amount["total_order_amount"] = (
    order_amount["total_product_amount"] +
    order_amount["total_freight_amount"]
)

# 保存每个订单的金额明细
order_amount.to_csv(
    OUTPUT_DIR / "03_order_amount_by_order.csv",
    index=False
)

# 对订单金额做基础统计
order_amount_distribution = (
    order_amount["total_order_amount"]
    .describe()
    .reset_index()
)

order_amount_distribution.columns = ["metric", "value"]

order_amount_distribution.to_csv(
    OUTPUT_DIR / "03_order_amount_distribution.csv",
    index=False
)

print("Order amount distribution saved.")

print("\nOrder analysis completed successfully.")