import os
import gzip
import shutil
import snowflake.connector

# 🔑 Credentials
USER = os.getenv("SNOWFLAKE_USER")
PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
WAREHOUSE = "COMPUTE_WH"
DATABASE = "IOWA_SALES_DB"
SCHEMA = "PUBLIC"
TABLE = "LIQUOR_SALES"
STAGE = "IOWA_STAGE"

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

# 🏗️ Setup DB + stage
cs.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
cs.execute(f"USE DATABASE {DATABASE}")
cs.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
cs.execute(f"USE SCHEMA {SCHEMA}")
cs.execute(f"CREATE OR REPLACE STAGE {STAGE}")

# Compress CSV
input_file = os.path.join(os.getcwd(), 'data/iowa_liquor_sales.csv')
gz_file = input_file + '.gz'

print("🔄 Compressing CSV...")
with open(input_file, 'rb') as f_in:
    with gzip.open(gz_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
print(f"✅ Compressed file saved to {gz_file}")

# Upload to stage
print("⬆️ Uploading to internal stage...")
cs.execute(f"PUT file://{os.path.abspath(gz_file)} @{STAGE} AUTO_COMPRESS=TRUE")

# Run COPY INTO
print("🚀 Loading data into Snowflake...")
cs.execute(f"""
COPY INTO {TABLE}
FROM @{STAGE}/iowa_liquor_sales.csv.gz
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
ON_ERROR = 'CONTINUE'
""")

# Check load history
print("📊 Load history:")
cs.execute(f"""
SELECT * FROM INFORMATION_SCHEMA.LOAD_HISTORY
WHERE table_name = '{TABLE.upper()}'
ORDER BY LAST_LOAD_TIME DESC
LIMIT 5
""")
for row in cs.fetchall():
    print(row)

# Optional cleanup
# cs.execute(f"REMOVE @{STAGE}/iowa_liquor_sales.csv.gz")

print("🎉 COPY INTO process complete!")
cs.close()
conn.close()
