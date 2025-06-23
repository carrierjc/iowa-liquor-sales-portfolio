import os
import sys
import math
import pandas as pd
import snowflake.connector

# 🔑 Get credentials from environment variables
USER = os.getenv("SNOWFLAKE_USER")
PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
WAREHOUSE = "COMPUTE_WH"
DATABASE = "IOWA_SALES_DB"
SCHEMA = "PUBLIC"
TABLE = "LIQUOR_SALES"

# ✅ Check credentials
if not USER or not PASSWORD or not ACCOUNT:
    print("❌ ERROR: Snowflake credentials are missing!")
    sys.exit(1)

# 🌐 Connect to Snowflake
try:
    print(f"Connecting to Snowflake as user: {USER}, account: {ACCOUNT}")
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE
    )
except Exception as e:
    print(f"❌ ERROR: Failed to connect to Snowflake: {e}")
    sys.exit(1)

cs = conn.cursor()

# 🏗️ Set up DB, schema, and table
try:
    cs.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
    cs.execute(f"USE DATABASE {DATABASE}")
    cs.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
    cs.execute(f"USE SCHEMA {SCHEMA}")

    cs.execute(f"""
    CREATE OR REPLACE TABLE {TABLE} (
        invoice_and_item_number STRING,
        date DATE,
        store_number INT,
        store_name STRING,
        address STRING,
        city STRING,
        zip_code STRING,
        store_location STRING,
        county_number INT,
        county STRING,
        category INT,
        category_name STRING,
        vendor_number INT,
        vendor_name STRING,
        item_number INT,
        item_description STRING,
        pack INT,
        bottle_volume_ml INT,
        state_bottle_cost FLOAT,
        state_bottle_retail FLOAT,
        bottles_sold INT,
        sale_dollars FLOAT,
        volume_sold_liters FLOAT,
        volume_sold_gallons FLOAT
    )
    """)
except Exception as e:
    print(f"❌ ERROR: Failed to set up DB/table: {e}")
    cs.close()
    conn.close()
    sys.exit(1)

# 📂 Read and insert data
csv_file = "data/iowa_liquor_sales.csv"
chunksize = 50000

numeric_cols = [
    'store_number', 'county_number', 'category', 'vendor_number',
    'item_number', 'pack', 'bottle_volume_ml', 'state_bottle_cost',
    'state_bottle_retail', 'bottles_sold', 'sale_dollars',
    'volume_sold_liters', 'volume_sold_gallons'
]

try:
    for chunk_idx, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunksize)):
        # Standardize and rename columns
        chunk.columns = [col.lower().strip() for col in chunk.columns]
        chunk.rename(columns={
            'invoice/item number': 'invoice_and_item_number',
            'bottle volume (ml)': 'bottle_volume_ml',
            'state bottle cost': 'state_bottle_cost',
            'state bottle retail': 'state_bottle_retail',
            'sale (dollars)': 'sale_dollars',
            'volume sold (liters)': 'volume_sold_liters',
            'volume sold (gallons)': 'volume_sold_gallons'
        }, inplace=True)

        # Convert numeric columns
        for col in numeric_cols:
            if col in chunk.columns:
                chunk[col] = pd.to_numeric(chunk[col], errors='coerce')

        # Convert date
        if 'date' in chunk.columns:
            chunk['date'] = pd.to_datetime(chunk['date'], errors='coerce')

        # Replace NaN with None
        chunk = chunk.where(pd.notnull(chunk), None)

        # Prepare insert
        insert_sql = f"INSERT INTO {TABLE} VALUES ({','.join(['%s'] * len(chunk.columns))})"

        # Insert rows safely
        for row in chunk.itertuples(index=False, name=None):
            row = list(row)

            # Format date
            date_idx = chunk.columns.get_loc('date')
            if row[date_idx] is not None:
                row[date_idx] = row[date_idx].strftime('%Y-%m-%d')

            # Replace NaN/nan-likes with None
            row = [
                None if (val is None or (isinstance(val, float) and math.isnan(val))) else val
                for val in row
            ]

            cs.execute(insert_sql, row)

        print(f"✅ Inserted chunk {chunk_idx + 1} with {len(chunk)} rows")

except Exception as e:
    print(f"❌ ERROR during data load: {e}")
    cs.close()
    conn.close()
    sys.exit(1)

# ✅ Finish up
print("🎉 Data load complete!")
cs.close()
conn.close()
