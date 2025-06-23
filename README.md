# Iowa Liquor Sales Data Portfolio Project

This project showcases my ability to work with large-scale datasets (30M+ records), build pipelines into Snowflake, analyze and summarize data using Python, and visualize insights using Power BI Online connected to Excel extracts.

---

## 🚀 Project Overview

✅ **Loaded 30M+ Iowa liquor sales records into Snowflake using Python**  
✅ **Aggregated and extracted data summaries with Python queries**  
✅ **Created Excel files with pivot tables and charts**  
✅ **Built interactive dashboards using Power BI Online connected to Excel extracts**

---

## 💻 Tools & Technologies

- **Python** (pandas, snowflake-connector-python)
- **Snowflake** (cloud data warehouse)
- **Excel** (pivot tables, charts)
- **Power BI Online** (interactive dashboards)

---

## 📂 Repository Structure

iowa-liquor-sales-portfolio/
├── data/ # Raw CSV data files (local use, not uploaded)
├── scripts/ # Python scripts (data loading, querying, exporting)
├── excel/ # Excel outputs: pivots, summaries, charts
├── outputs/ # Validation reports, other output files
├── README.md # This file


---

## ⚙ Project Steps

1️⃣ **Data ingestion**  
- Used Python to compress and stage the CSV file  
- Loaded data into Snowflake efficiently using `COPY INTO`  

2️⃣ **Data validation**  
- Wrote Python scripts to check row counts, nulls, date ranges, and load history  
- Exported validation results to Excel  

3️⃣ **Data summaries**  
- Queried top city/category sales combinations (`extract_top_city_category.py`)  
- Analyzed time series of sales in liters and dollars by store and item (`extract_top_store_item.py`)  
- Exported all summaries to Excel  

4️⃣ **Visualization**  
- Connected Power BI Online to the Excel extracts  
- Built interactive dashboards (e.g., sales trends, top stores, top items)

---

## 📊 Example Insights

- Top cities and categories by total sales dollars  
- Time series trends of sales in liters and dollars by store and item  
- Store-level performance over time  

---

## 📝 Key Files

- `scripts/load_copy_into.py` → Python script to stage and load data into Snowflake  
- `scripts/extract_top_city_category.py` → Extracts top city/category sales summaries  
- `scripts/extract_top_store_item.py` → Extracts time series of sales by store and item  
- `scripts/validate_to_excel.py` → Runs validation queries and exports results to Excel  
- `excel/top_city_category_summary.xlsx` → Summary data for pivot/chart creation  
- `excel/top_store_item_timeseries.xlsx` → Store/item time series data  
- `outputs/validation_results.xlsx` → Validation report  

---

## 🌐 Power BI Online

Power BI dashboards were built using Power BI Service (cloud version).  
✅ Data source: Excel extracts generated from Python queries  
✅ Visualized sales trends, top stores, and top items using bar charts, line charts, and tables  

---

## 📌 Notes

- Data source: [Iowa Liquor Sales](https://data.iowa.gov/Economy/Iowa-Liquor-Sales/m3tr-qhgy)  
- This project focuses on demonstrating end-to-end data engineering + analytics workflows, not drawing business conclusions.

---

## 🤝 Let’s connect!

🔗 [My LinkedIn](https://www.linkedin.com/in/johnccarrier/) — I’m open to opportunities in data analytics and business intelligence!

