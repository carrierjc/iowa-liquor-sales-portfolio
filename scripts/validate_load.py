import os
import snowflake.connector

# 🔑 Credentials
USER = os.getenv("SNOWFLAKE_USER")
PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
WAREHOUSE = "COMPUTE_WH"
DATABASE = "IOWA_SALES_DB"
SCHEMA = "PUBLIC"
TABLE = "LIQUOR_SALES"

# ✅ Check credentials
if not USER or not PASSWORD or not ACCOUNT:
    raise Exception("❌ Missing Snowflake credentials!")

# 🌐 Connect
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
)
cs = conn.cursor()

# 🚀 Validation queries
queries = {
    "Row count": f"SELECT COUNT(*) FROM {TABLE}",
    "Sample rows": f"SELECT * FROM {TABLE} LIMIT 5",
    "NULL checks": f"""
        SELECT
          COUNT(*) AS total_rows,
          COUNT_IF(date IS NULL) AS null_dates,
          COUNT_IF(store_number IS NULL) AS null_store_numbers,
          COUNT_IF(sale_dollars IS NULL) AS null_sales
        FROM {TABLE}
    """,
    "Date range": f"SELECT MIN(date), MAX(date) FROM {TABLE}",
    "Top categories": f"""
        SELECT category_name, COUNT(*) AS row_count, SUM(sale_dollars) AS total_sales
        FROM {TABLE}
        GROUP BY category_name
        ORDER BY total_sales DESC
        LIMIT 5
    """,
    "Recent load history": f"""
        SELECT table_name, file_name, row_count, error_count, status, last_load_time
        FROM INFORMATION_SCHEMA.LOAD_HISTORY
        WHERE table_name = '{TABLE.upper()}'
        ORDER BY last_load_time DESC
        LIMIT 3
    """
}

# 🔍 Run queries
for name, query in queries.items():
    print(f"\n🔹 {name}")
    cs.execute(query)
    rows = cs.fetchall()
    for row in rows:
        print(row)

# ✅ Done
cs.close()
conn.close()
print("\n🎉 Validation complete!")
