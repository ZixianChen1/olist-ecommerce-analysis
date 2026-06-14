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
# 2.1 Check and handle missing product categories
# =========================

# Check products with missing product category
missing_category_products = products[products["product_category_name"].isnull()]

print("Missing product category count:", len(missing_category_products))
print("Is product_id unique in products table:", products["product_id"].is_unique)

# Since product_id is unique in the products table,
# missing categories cannot be recovered from another row with the same product_id.
# Other fields, such as product name length, description length,
# photo quantity, weight and size, are not enough to reliably infer the exact category.
# Therefore, unrecoverable missing categories are labelled as "Unknown".
products["product_category_name"] = products["product_category_name"].fillna("Unknown")

# =========================
# 3. Total number of products and categories
# =========================

total_products = products["product_id"].nunique()

# After filling missing categories as "Unknown",
# total_categories includes "Unknown" as one category.
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

# order_items table has one row for each product item in an order.
# Therefore, counting product_id can be used as product sales volume.
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

# Merge order_items with products by product_id.
# This allows each order item to be linked with its product category.
order_items_with_category = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# If there are product_ids in order_items that do not exist in products,
# their categories will still be missing after the merge.
# Label these remaining missing categories as "Unknown" as well.
order_items_with_category["product_category_name"] = (
    order_items_with_category["product_category_name"].fillna("Unknown")
)

# Count sales volume by product category
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

# price is the product sales amount.
# Summing price by category gives the total revenue of each product category.
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