import pandas as pd
import sqlite3
from pathlib import Path

# =========================
# 1. Set file paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "olist_ecommerce.db"
SQL_DIR = BASE_DIR / "sql_scripts"
OUTPUT_DIR = BASE_DIR / "output_csv" / "sql_results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# 2. Define SQL files
# =========================

sql_files = [
    "01_data_check.sql",
    "02_customer_analysis.sql",
    "03_order_analysis.sql",
    "04_product_analysis.sql",
    "05_seller_analysis.sql",
    "06_join_queries.sql"
]

# =========================
# 3. Connect to SQLite database
# =========================

conn = sqlite3.connect(DB_PATH)

print(f"Connected to database: {DB_PATH}")

# =========================
# 4. Run each SQL file
# =========================

for sql_file in sql_files:
    sql_path = SQL_DIR / sql_file

    print(f"\nRunning SQL file: {sql_file}")

    with open(sql_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Remove SQL comment lines
    sql_lines = []
    for line in lines:
        stripped_line = line.strip()

        # Skip empty lines and comment lines
        if stripped_line == "":
            continue
        if stripped_line.startswith("--"):
            continue

        sql_lines.append(line)

    sql_content = "".join(sql_lines)

    # Split SQL content by semicolon
    queries = [
        query.strip()
        for query in sql_content.split(";")
        if query.strip()
    ]

    file_prefix = sql_file.replace(".sql", "")

    for i, query in enumerate(queries, start=1):
        try:
            result = pd.read_sql_query(query, conn)

            output_file = OUTPUT_DIR / f"{file_prefix}_query_{i}.csv"
            result.to_csv(output_file, index=False)

            print(f"Saved: {output_file.name}, rows: {len(result)}")

        except Exception as e:
            print(f"Error in {sql_file}, query {i}: {e}")

# =========================
# 5. Close connection
# =========================

conn.close()

print("\nAll SQL scripts executed successfully.")