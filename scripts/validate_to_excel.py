import os
import snowflake.connector
import pandas as pd

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
    "Row count": f"SELECT COUNT(*) AS total_rows FROM {TABLE}",
    "Sample rows": f"SELECT * FROM {TABLE} LIMIT 5",
    "NULL checks": f"""
        SELECT
          COUNT(*) AS total_rows,
          COUNT_IF(date IS NULL) AS null_dates,
          COUNT_IF(store_number IS NULL) AS null_store_numbers,
          COUNT_IF(sale_dollars IS NULL) AS null_sales
        FROM {TABLE}
    """,
    "Date range": f"SELECT MIN(date) AS min_date, MAX(date) AS max_date FROM {TABLE}",
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

# 📝 Collect results
output = {}

from pandas.api.types import DatetimeTZDtype

# 📝 Collect results
output = {}

for name, query in queries.items():
    print(f"Running: {name}")
    cs.execute(query)
    df = pd.DataFrame(cs.fetchall(), columns=[col[0] for col in cs.description])

    # Remove timezone info from datetime columns
    for col in df.columns:
        if isinstance(df[col].dtype, DatetimeTZDtype):
            df[col] = df[col].dt.tz_localize(None)

    output[name] = df


# 📂 Export to Excel
output_file = "outputs/validation_results.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for name, df in output.items():
        sheet_name = name[:31]  # Excel max sheet name length
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"🎉 Validation results exported to {output_file}")

cs.close()
conn.close()
