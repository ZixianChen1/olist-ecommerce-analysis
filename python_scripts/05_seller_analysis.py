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

sellers = pd.read_csv(DATA_DIR / "olist_sellers_dataset.csv")
order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")

print("Sellers table shape:", sellers.shape)
print("Order items table shape:", order_items.shape)

# =========================
# 3. Total number of sellers
# =========================

total_sellers = sellers["seller_id"].nunique()

total_sellers_result = pd.DataFrame({
    "metric": ["total_sellers"],
    "value": [total_sellers]
})

total_sellers_result.to_csv(
    OUTPUT_DIR / "05_total_sellers.csv",
    index=False
)

print("Total sellers saved.")

# =========================
# 4. Seller distribution by state
# =========================

sellers_by_state = (
    sellers
    .groupby("seller_state")
    .size()
    .reset_index(name="seller_count")
    .sort_values(by="seller_count", ascending=False)
)

sellers_by_state.to_csv(
    OUTPUT_DIR / "05_sellers_by_state.csv",
    index=False
)

print("Seller distribution by state saved.")

# =========================
# 5. Seller order volume Top 10
# =========================

# order_items 表中每一行代表一个订单商品
# 一个 seller_id 可能对应多个订单商品
# 这里先统计每个卖家的订单商品行数
seller_order_volume = (
    order_items
    .groupby("seller_id")
    .agg(
        order_item_count=("order_id", "count"),
        unique_order_count=("order_id", "nunique")
    )
    .reset_index()
)

# 关联 sellers 表，补充卖家城市和州
seller_order_volume = seller_order_volume.merge(
    sellers[["seller_id", "seller_city", "seller_state"]],
    on="seller_id",
    how="left"
)

seller_order_volume_top10 = (
    seller_order_volume
    .sort_values(by="unique_order_count", ascending=False)
    .head(10)
)

seller_order_volume_top10.to_csv(
    OUTPUT_DIR / "05_seller_order_volume_top10.csv",
    index=False
)

print("Seller order volume Top 10 saved.")

# =========================
# 6. Seller revenue Top 10
# =========================

# price 是订单商品金额
# freight_value 是运费
# 这里销售额主要按商品金额 price 统计
seller_revenue = (
    order_items
    .groupby("seller_id")
    .agg(
        total_revenue=("price", "sum"),
        total_freight=("freight_value", "sum"),
        order_item_count=("order_id", "count"),
        unique_order_count=("order_id", "nunique")
    )
    .reset_index()
)

# 关联 sellers 表，补充卖家城市和州
seller_revenue = seller_revenue.merge(
    sellers[["seller_id", "seller_city", "seller_state"]],
    on="seller_id",
    how="left"
)

seller_revenue_top10 = (
    seller_revenue
    .sort_values(by="total_revenue", ascending=False)
    .head(10)
)

seller_revenue_top10.to_csv(
    OUTPUT_DIR / "05_seller_revenue_top10.csv",
    index=False
)

print("Seller revenue Top 10 saved.")

print("\nSeller analysis completed successfully.")