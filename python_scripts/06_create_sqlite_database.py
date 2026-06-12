import pandas as pd
import sqlite3
from pathlib import Path

# =========================
# 1. Set file paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "olist_ecommerce.db"

# =========================
# 2. Define CSV files and table names
# =========================

files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv"
}

# =========================
# 3. Create SQLite database connection
# =========================

# 如果 olist_ecommerce.db 不存在，sqlite3 会自动创建
# 如果已经存在，它会连接到这个数据库
conn = sqlite3.connect(DB_PATH)

print(f"SQLite database connected: {DB_PATH}")

# =========================
# 4. Load CSV files into SQLite tables
# =========================

for table_name, file_name in files.items():
    file_path = DATA_DIR / file_name

    print(f"\nLoading {file_name} into table: {table_name}")

    df = pd.read_csv(file_path)

    # 把 DataFrame 写入 SQLite 数据库
    # if_exists="replace" 表示如果表已经存在，就覆盖
    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Table {table_name} loaded successfully. Shape: {df.shape}")

# =========================
# 5. Create indexes
# =========================

# SQLite 中不一定强制设置主键
# 这里先创建索引，提高后续 SQL 查询效率
# 同时也满足任务里“创建主键索引”的要求

cursor = conn.cursor()

index_sql_list = [
    "CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id);",
    "CREATE INDEX IF NOT EXISTS idx_customers_unique_id ON customers(customer_unique_id);",
    "CREATE INDEX IF NOT EXISTS idx_orders_order_id ON orders(order_id);",
    "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);",
    "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);",
    "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);",
    "CREATE INDEX IF NOT EXISTS idx_order_items_seller_id ON order_items(seller_id);",
    "CREATE INDEX IF NOT EXISTS idx_products_product_id ON products(product_id);",
    "CREATE INDEX IF NOT EXISTS idx_sellers_seller_id ON sellers(seller_id);"
]

for sql in index_sql_list:
    cursor.execute(sql)

conn.commit()

print("\nIndexes created successfully.")

# =========================
# 6. Check imported tables
# =========================

for table_name in files.keys():
    query = f"SELECT COUNT(*) AS row_count FROM {table_name};"
    result = pd.read_sql_query(query, conn)
    print(f"{table_name}: {result.loc[0, 'row_count']} rows")

# =========================
# 7. Close database connection
# =========================

conn.close()

print("\nSQLite database creation completed successfully.")