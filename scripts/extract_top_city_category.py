import os
import snowflake.connector
import pandas as pd

# 🔑 Snowflake credentials
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

# 🌐 Connect to Snowflake
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
)
cs = conn.cursor()

# 📊 Query top city/category sales
query = f"""
SELECT 
  year(i.date) as sales_year,
  i.city,
  i.category_name,
  SUM(i.volume_sold_liters) AS total_sales_liters,
  SUM(i.sale_dollars) AS total_sales_dollars
FROM {TABLE} i
GROUP BY sales_year, i.city, i.category_name
ORDER BY total_sales_dollars DESC
"""

print("🚀 Running query...")
cs.execute(query)

# Fetch results into DataFrame
df = pd.DataFrame(cs.fetchall(), columns=[col[0] for col in cs.description])

# 💾 Save to Excel
output_file = "excel/top_city_category_summary.xlsx"
df.to_excel(output_file, index=False)
print(f"🎉 Summary exported to {output_file}")

cs.close()
conn.close()
