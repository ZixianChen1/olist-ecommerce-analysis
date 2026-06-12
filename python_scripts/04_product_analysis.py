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

products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")
order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")

print("Products table shape:", products.shape)
print("Order items table shape:", order_items.shape)

# =========================
# 3. Total number of products and categories
# =========================

total_products = products["product_id"].nunique()
total_categories = products["product_category_name"].nunique()

product_summary = pd.DataFrame({
    "metric": ["total_products", "total_categories"],
    "value": [total_products, total_categories]
})

product_summary.to_csv(
    OUTPUT_DIR / "04_product_summary.csv",
    index=False
)

print("Product summary saved.")

# =========================
# 4. Product count by category
# =========================

products_by_category = (
    products
    .groupby("product_category_name")
    .size()
    .reset_index(name="product_count")
    .sort_values(by="product_count", ascending=False)
)

products_by_category.to_csv(
    OUTPUT_DIR / "04_products_by_category.csv",
    index=False
)

print("Products by category saved.")

# =========================
# 5. Product sales ranking
# =========================

# order_items 表中每一行代表一个订单商品
# 所以按 product_id 统计出现次数，可以理解为商品销量
product_sales_ranking = (
    order_items
    .groupby("product_id")
    .size()
    .reset_index(name="sales_count")
    .sort_values(by="sales_count", ascending=False)
)

product_sales_ranking.to_csv(
    OUTPUT_DIR / "04_product_sales_ranking.csv",
    index=False
)

print("Product sales ranking saved.")

# =========================
# 6. Category sales ranking
# =========================

# 把 order_items 和 products 通过 product_id 关联
# 这样每个订单商品就能对应到商品类目
order_items_with_category = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# 按类目统计销量
category_sales_count = (
    order_items_with_category
    .groupby("product_category_name")
    .size()
    .reset_index(name="sales_count")
    .sort_values(by="sales_count", ascending=False)
)

category_sales_count.to_csv(
    OUTPUT_DIR / "04_category_sales_count.csv",
    index=False
)

print("Category sales count saved.")

# =========================
# 7. Category revenue ranking
# =========================

# price 是商品销售金额
# 按类目汇总 price，可以得到类目销售额
category_revenue_ranking = (
    order_items_with_category
    .groupby("product_category_name")
    .agg(
        total_revenue=("price", "sum"),
        total_sales_count=("product_id", "count")
    )
    .reset_index()
    .sort_values(by="total_revenue", ascending=False)
)

category_revenue_ranking.to_csv(
    OUTPUT_DIR / "04_category_revenue_ranking.csv",
    index=False
)

print("Category revenue ranking saved.")

print("\nProduct analysis completed successfully.")