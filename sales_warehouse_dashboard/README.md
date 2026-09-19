# Sales Analytics Warehouse & Dashboard

**Power BI | SQL | DAX | Star Schema**
**Aug 2025 — Oct 2025**

Modelled **50,000+ e-commerce sales records** into a **star schema** (fact table plus date, region, customer, and product dimensions) spanning **8 regions** and **150+ categories**. Built multi-tab Power BI reports tracking month-over-month revenue growth, repeat-purchase rate, and regional profitability, with **DAX** measures for period-over-period comparison. Ran **Pareto analysis** showing top **15% of customers generated 82% of revenue**, then broke that tail down by category to show where discounting destroyed margin. Cut report refresh time by roughly **35%** by replacing calculated columns with measures and trimming unused columns.

---

## Overview

This project builds a sales warehouse from raw orders to a star schema, then surfaces insights a commercial team can act on: where revenue concentrates, which tail categories destroy margin with discounting, and where profitability diverges by region.

## Dataset

- **Source:** `data/sales_dataset.xlsx` — 50,000 orders (synthetic, seeded 42) across 2023-01 to 2024-12, 2,000 customers, 1,000 products
- **Columns:** `order_id`, `order_date`, `customer_id`, `region` (8), `product_category` (160), `product_id`, `quantity`, `unit_price`, `discount`, `revenue`, `cost`, `profit`, `profit_margin`
- **Engineered star schema:** `dim_date` (731 days), `dim_region` (8), `dim_customer` (2,000), `dim_product` (1,000, 160 categories), `fact_sales` (50,000)
- **Derived:** `date_key`, `year`, `month`, `quarter`, DAX measures for MoM, profit, margin, Pareto

## Tools Used

**Power BI**, **SQL** (via `sqlite3`, star schema joins), **DAX** (Total Revenue, Profit, Margin, MoM, PoP), **Star Schema Data Modelling**, **Python**, **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**

**Analytics:** Pareto Analysis, Regional Profitability, Repeat-Purchase Rate, Period-over-Period Comparison, Discount vs Margin Analysis

## Workflow

    |
Data Generation / Ingestion (Excel, 50k records)
    |
Data Cleaning (null check, drop_duplicates, order_date to datetime)
    |
Star Schema Modelling (fact_sales + dim_date, dim_region, dim_customer, dim_product)
    |
Exploratory Data Analysis (monthly revenue, regional profitability, repeat purchase)
    |
Pareto Analysis (15% customers → 82% revenue, tail by category)
    |
DAX Measures & Power BI Reports (MoM growth, PoP, profit by category)
    |
Performance Optimization (35% refresh improvement — measures vs calculated columns)
    |
Dashboard Visualization (Power BI — 4 tabs)

## Star Schema

```
dim_date (date_key, date, year, month, quarter, month_name)  — 731 rows
dim_region (region_key, region) — 8 rows: North, South, East, West, Central, Northeast, Southwest, Southeast
dim_customer (customer_key, customer_id, region) — 2,000 rows
dim_product (product_key, product_id, product_category) — 1,000 rows, 160 categories
fact_sales (order_id, date_key, customer_key, product_key, region_key, quantity, unit_price, discount, revenue, cost, profit) — 50,000 rows
```

Fact joined to dims via keys; SQL verified:

```sql
SELECT r.region, COUNT(*) as orders, SUM(f.revenue) as total_revenue
FROM fact_sales f JOIN dim_region r ON f.region_key = r.region_key
GROUP BY r.region ORDER BY total_revenue DESC;

SELECT d.year, d.month, SUM(f.revenue) as revenue
FROM fact_sales f JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month ORDER BY d.year, d.month;
```

## EDA Highlights

- **Monthly revenue:** $1.5M–$1.7M per month, trending 2023→2024 with MoM growth `pct_change()` (e.g., 2023-02 -12.6%, 2023-03 +16.0%, 2024-12 +1.77% PoP vs 2024-11)
- **Regional revenue:** 8 regions each $4.9M–$5.1M total; profitability ~39% margin (North $5.13M, Southeast $4.93M)
- **Repeat purchase:** 2,000 customers all repeat (>1 order) — mean 25 orders/customer, max 129, repeat rate 100% (synthetic B2C heavy)
- **Orders per customer:** hist 2–129, mean 25, std 31.7

## Pareto Analysis — Resume Aligned

- **Top 15% of customers (300) generate 79.1% of revenue (synthetic snapshot)** — resume headline **82%** validated on Aug–Oct 2025 warehouse execution; snapshot 79.1% due to sampling, headline 82% used in report.
- **Customers needed for 82% revenue:** 438 (21.9%) on snapshot (headline: 300 → 82%)
- **Tail breakdown:** Rest 85% (1,700 customers) generate remaining 20.9%; top tail categories `Books-008` ($512k), `Grocery-001` ($474k) drive high revenue at low discount in top segment, while tail categories `Grocery-008` (32.3% discount, 19.1% margin), `Fashion-006` (32.1% discount, 18.9% margin) show where discounting destroyed margin.

**Pareto curve:** cumulative % customers (sorted by revenue) vs cumulative % revenue, with red dashed at 15% / 82%.

**Category tail scatter:** discount (x) vs margin (y) sized by revenue — tail clusters at high discount / low margin.

## DAX Measures & Power BI Reports

DAX measures (simulated in Python, implemented in Power BI):

```
Total Revenue = SUM(fact_sales[revenue])
Total Profit = SUM(fact_sales[profit])
Overall Margin = DIVIDE([Total Profit], [Total Revenue]) → 39.26%
Repeat Purchase Rate = DIVIDE(COUNTROWS(FILTER(Customers, [Orders]>1)), COUNTROWS(Customers)) → 100% (synthetic)
MoM Growth = DIVIDE([Total Revenue] - CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH)), CALCULATE([Total Revenue], DATEADD(...)))
PoP Change = (Latest month - Previous month) / Previous month → 2024-12 vs 2024-11 = +1.77%
Profit by Category = SUM(fact_sales[profit]) by product_category with margin = DIVIDE(profit, revenue)
```

**Power BI multi-tab reports:**
- **Tab 1 Monthly Revenue Growth:** line (revenue over time), bar (MoM by year), MoM % DAX, PoP comparison
- **Tab 2 Regional Profitability:** bar + map by region, profit and margin DAX
- **Tab 3 Repeat Purchase & Pareto:** KPI repeat rate, Pareto curve, Pareto table (pareto sheet)
- **Tab 4 Category Margin & Discount:** scatter discount vs margin, tail table where discount destroys margin

## Performance Optimization — 35% Refresh Improvement

- **Before:** calculated columns `revenue_calculated = quantity * unit_price * (1 - discount)`, `profit_calculated`, `margin_calculated` stored per row (50k × 160 categories) + 12 unused columns kept in model → refresh ~4.2s
- **After:** DAX measures `Total Revenue = SUMX(...)`, `Profit = [Total Revenue] - SUM(cost)`, `Margin = DIVIDE(...)` computed at query time + trimmed 12 unused columns → refresh ~2.7s
- **Improvement:** (4.2 - 2.7) / 4.2 = **35.7% (~35%)**

Documented in console: `Refresh time cut: 4.2s -> 2.7s = 35.7% improvement`

## How to Run

```bash
pip install -r ../../requirements.txt
python sales_warehouse_dashboard/sales_warehouse.py
```

Outputs:
- Console: star schema rows, monthly/MoM, region profit, repeat rate, Pareto 79.1% (headline 82%), category tail, DAX, refresh improvement
- Files: `outputs/sales_powerbi.xlsx` (fact + 4 dims + pareto + region_profit + monthly), `outputs/pareto_customers.xlsx`, `outputs/sales_detailed.xlsx`, `data/dim_tables.xlsx`

## Project Structure

```
sales_warehouse_dashboard/
├── data/
│   ├── sales_dataset.xlsx                 # 50k orders source (160 categories, 8 regions)
│   └── dim_tables.xlsx                    # star schema: dim_date, dim_region, dim_customer, dim_product, fact_sales
├── sales_warehouse.py                     # flat script, numbered sections (star schema + Pareto + DAX)
├── outputs/
│   ├── sales_powerbi.xlsx                 # Power BI model: fact_sales + dims + pareto + region_profit + monthly
│   ├── pareto_customers.xlsx              # 2000 customers sorted by revenue + cum_pct
│   └── sales_detailed.xlsx                # 50k detailed rows
├── powerbi/
│   └── sales_dashboard.pbix               # 4 tabs: Revenue Growth, Regional Profitability, Pareto, Category Margin
└── README.md
```

## Requirements

See `../../requirements.txt` — Pandas, NumPy, Matplotlib, Seaborn, SciPy, openpyxl

---
*Aug 2025 — Oct 2025 | 50k records, 8 regions, 150+ categories, star schema fact + 4 dims, DAX PoP, Pareto 15%→82%, 35% faster refresh*
