import pandas as pd
from pathlib import Path

# =========================
# 1. Set file paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output_csv"

OUTPUT_DIR.mkdir(exist_ok=True)

files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv"
}

primary_keys = {
    "customers": "customer_id",
    "orders": "order_id",
    "order_items": None,
    "products": "product_id",
    "sellers": "seller_id"
}

# =========================
# 2. Load 5 tables
# =========================

tables = {}

for name, file_name in files.items():
    file_path = DATA_DIR / file_name
    tables[name] = pd.read_csv(file_path)
    print(f"\n========== {name.upper()} ==========")
    print(f"Shape: {tables[name].shape}")

# =========================
# 3. Check first 5 rows
# =========================

for name, df in tables.items():
    print(f"\n\n===== First 5 rows of {name} =====")
    print(df.head())

# =========================
# 4. Check data types
# =========================

dtype_results = []

for name, df in tables.items():
    temp = pd.DataFrame({
        "table_name": name,
        "column_name": df.columns,
        "data_type": df.dtypes.astype(str).values
    })
    dtype_results.append(temp)

dtype_results = pd.concat(dtype_results, ignore_index=True)
dtype_results.to_csv(OUTPUT_DIR / "01_data_types.csv", index=False)

print("\nData types saved to output_csv/01_data_types.csv")

# =========================
# 5. Check missing values
# =========================

missing_results = []

for name, df in tables.items():
    temp = pd.DataFrame({
        "table_name": name,
        "column_name": df.columns,
        "missing_count": df.isnull().sum().values,
        "missing_ratio": df.isnull().mean().values
    })
    missing_results.append(temp)

missing_results = pd.concat(missing_results, ignore_index=True)
missing_results.to_csv(OUTPUT_DIR / "01_missing_values.csv", index=False)

print("Missing values saved to output_csv/01_missing_values.csv")

# =========================
# 6. Check primary key uniqueness
# =========================

pk_results = []

for name, df in tables.items():
    pk = primary_keys[name]

    if pk is None:
        pk_results.append({
            "table_name": name,
            "primary_key": "No single primary key",
            "total_rows": len(df),
            "unique_values": None,
            "is_unique": None
        })
    else:
        pk_results.append({
            "table_name": name,
            "primary_key": pk,
            "total_rows": len(df),
            "unique_values": df[pk].nunique(),
            "is_unique": df[pk].is_unique
        })

pk_results = pd.DataFrame(pk_results)
pk_results.to_csv(OUTPUT_DIR / "01_primary_key_check.csv", index=False)

print("Primary key check saved to output_csv/01_primary_key_check.csv")

print("\nAll basic data checks completed successfully.")