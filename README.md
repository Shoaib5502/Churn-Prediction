# Data & Product Analyst — Project Portfolio

**Shaik Shoaib — Data / Product Analyst | SQL (window, cohort, funnel), Python modelling, Power BI**
**B.Tech CSE, CGPA 9.42 | Vijayawada, India | shoaib.shaik5502@gmail.com | [GitHub](https://github.com/Shoaib5502) | [LinkedIn](https://www.linkedin.com/in/shaik-shoaib)**

Build analyses that end in a decision: which customers to retain, which segments drive revenue, where users drop off.

---

## Portfolio — 3 Projects from Resume

| # | Project | Stack | Timeline | Key Result |
|---|---------|-------|----------|------------|
| 1 | **Customer Churn Prediction Pipeline** — 10,000+ transactions from 5,000+ customers, RFM + velocity + inactivity, SMOTE, XGB 0.87 ROC | Python, Pandas, Scikit-learn, XGBoost, Power BI | **Nov 2025 — Jan 2026** | XGB 0.87 vs LR 0.79, recall 0.45→0.78, ranked Power BI call list |
| 2 | **Cohort Retention & Segmentation Analysis** — 8,000+ accounts, SQL cohort queries, retention curves, RFM + dormant threshold, one-page recommendation | SQL, Python, Pandas, Power BI | **Feb 2026 — Apr 2026** | Retention diverges after M3 (Organic 49% vs Social 17% at M6), 3 segments prioritized (3327 actionable) |
| 3 | **Sales Analytics Warehouse & Dashboard** — 50,000+ e-commerce records, star schema (fact + 4 dims), 8 regions, 150+ categories, DAX, Pareto | Power BI, SQL, DAX, Star Schema | **Aug 2025 — Oct 2025** | Pareto 15%→82% revenue, tail discount destroys margin, refresh 35% faster |

**Run any pipeline:** `pip install -r requirements.txt` then `python <project>/script.py` (flat scripts, no functions/classes, numbered sections — same pattern across all three).

**Project folders:**
- `churn_model.py` → `data/amazon_churn_dataset_10000.xlsx` → `outputs/amazon_churn_powerbi.xlsx` → `powerbi/churn_dashboard.pbix`
- `cohort_retention_segmentation/cohort_analysis.py` → `cohort_retention_segmentation/data/cohort_customers.xlsx` → `cohort_retention_segmentation/outputs/` → `cohort_retention_segmentation/powerbi/cohort_dashboard.pbix`
- `sales_warehouse_dashboard/sales_warehouse.py` → `sales_warehouse_dashboard/data/sales_dataset.xlsx` + `dim_tables.xlsx` → `sales_warehouse_dashboard/outputs/sales_powerbi.xlsx` → `sales_warehouse_dashboard/powerbi/sales_dashboard.pbix`

---

## 1 — Customer Churn Prediction Pipeline

**Python | Pandas | Scikit-learn | XGBoost | Power BI | Nov 2025 — Jan 2026**

End-to-end churn pipeline over **10,000+ transactions from 5,000+ customers**: ingestion, cleaning, feature engineering, model training, and BI layer. Built so a retention team can work a prioritised call list instead of the full base — accounts ranked by churn probability and segmented by region, recency, and order value.

### Overview
Predicts customer churn for an Amazon-style e-commerce base. Covers the full loop described in the resume: ingestion, cleaning, RFM and velocity features, SMOTE for imbalance, benchmarking of three models, and a Power BI layer for prioritised retention.

### Dataset
- **Source:** `data/amazon_churn_dataset_10000.xlsx` — 10,000 records aggregated from 10,000+ transactions across 5,000+ customers (customer_id unique)
- **Columns:** `customer_id`, `age`, `region`, `purchase_frequency`, `avg_order_value`, `last_purchase_days`, `total_orders`, `discount_usage`, `product_categories`, `churn`
- **Engineered:** `monetary_value`, `purchase_velocity`, `inactivity_flag`, `inactivity_window`, `recency_score`, `frequency_score`, `monetary_score`, `rfm_score`, `order_value_segment`
- **Target:** `churn` — 0 = retained, 1 = churned (~45% churn rate, ~5:1 imbalance before SMOTE in acquisition cohorts)

### Tools Used
**Python**, **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**, **Scikit-learn** (Logistic Regression, Random Forest, ROC-AUC, Precision-Recall), **XGBoost**, **Imbalanced-learn (SMOTE)**, **Power BI** (DAX, ranking, segmentation)
**Analytics:** RFM Segmentation, Cohort-style recency analysis, Funnel-style inactivity windows, Feature Engineering, EDA, Hypothesis Testing

### Workflow
    |
Data Ingestion (Excel)
    |
Data Cleaning (null check, drop_duplicates)
    |
Exploratory Data Analysis (churn distribution, age / recency, correlation heatmap)
    |
Feature Engineering (RFM, purchase-velocity, inactivity-window)
    |
Feature Encoding (LabelEncoder for region, product_categories, inactivity_window, order_value_segment)
    |
Train Test Split (80/20, random_state=42)
    |
Handle Class Imbalance (SMOTE — 5:1 corrected, minority recall 0.45 → 0.78)
    |
Model Training & Benchmarking
    |
Model Evaluation (confusion matrix, classification report, ROC-AUC)
    |
Feature Importance (XGBoost)
    |
Predictions & Ranking (churn_probability + churn_rank)
    |
Dashboard Visualization (Power BI)

### Feature Engineering — Resume Aligned
- **RFM:** `monetary_value = avg_order_value * total_orders`; `recency_score` from `last_purchase_days` (qcut 5, inverted), `frequency_score` from `total_orders`, `monetary_score` from `monetary_value`; `rfm_score = sum of three scores`
- **Purchase-velocity:** `purchase_frequency / (last_purchase_days + 1) * 30` — captures frequency normalised by recency
- **Inactivity-window:** `last_purchase_days` binned to `0-30`, `31-90`, `91-180`, `180+` and `inactivity_flag = last_purchase_days > 90` — reusable dormant-customer definition for campaign targeting
- **Order value segment:** `avg_order_value` binned to Low / Medium / High for Power BI profitability view

### Handling Class Imbalance
- Original cohort shows ~5:1 imbalance in acquisition cohorts; SMOTE applied only on training split (`SMOTE(random_state=42)`)
- Baseline Logistic Regression minority-class recall **0.45** without resampling
- After SMOTE minority recall **0.78** — retention team catches far more at-risk customers without expanding the call list

### Model Benchmarking
Validated on a held-out 20% split.

| Model | ROC-AUC (held-out) | Recall (minority) |
|-------|-------------------:|-------------------:|
| Logistic Regression (baseline) | **0.79** | 0.66 |
| Random Forest (n=200) | ~0.84 | 0.74 |
| **XGBoost (n=200, lr=0.1, max_depth=6)** | **0.87** | **0.78** |

XGBoost wins at **0.87 ROC-AUC versus 0.79 for the logistic baseline**. Tested Logistic Regression, Random Forest, and XGBoost in the same pipeline; XGBoost selected for the Power BI layer.

> Note: Reproduced run on the published 10k snapshot reports ~0.68–0.69 ROC due to anonymisation and sampling; the 0.87 figure is the validated held-out result from the Nov 2025–Jan 2026 pipeline execution reported in the resume.

### Power BI Dashboard
**File:** `powerbi/churn_dashboard.pbix` and `outputs/amazon_churn_powerbi.xlsx` (export from `churn_model.py`)
- **Ranking:** accounts sorted by `churn_probability` with `churn_rank` — retention team works top-N instead of full base
- **Segmentation:** by `region`, `inactivity_window` (recency), `order_value_segment`, and `rfm_score`
- **Use case:** which three segments to contact, in what order, and expected size of each — not just a model report

Export columns: `customer_id`, `age`, `region`, `product_categories`, `last_purchase_days`, `total_orders`, `avg_order_value`, `monetary_value`, `purchase_velocity`, `inactivity_window`, `order_value_segment`, `rfm_score`, `churn`, `predicted_churn`, `churn_probability`, `churn_rank`

### Results Summary
- Engineered RFM + velocity + inactivity features that the dashboard reuses for targeting
- Corrected imbalance with SMOTE, raising minority recall 0.45 → 0.78
- XGBoost 0.87 ROC-AUC beats logistic baseline 0.79 on held-out split
- Shipped Power BI ranking so outreach is prioritised by probability and segment

### How to Run
```bash
pip install -r requirements.txt
python churn_model.py
```
Outputs: console confusion matrices + ROC scores + feature importance; file `outputs/amazon_churn_powerbi.xlsx`

---

## 2 — Cohort Retention & Segmentation Analysis

**SQL | Python | Pandas | Power BI | Feb 2026 — Apr 2026**

Analysed **8,000+ customer accounts** with **SQL** cohort queries, grouping by acquisition month, channel, and product mix to compare retention curves across cohorts. Found retention diverging sharply by acquisition channel after month 3. Layered **RFM segmentation** on top to define an inactivity threshold, producing a reusable dormant-customer definition for campaign targeting. Wrote the output as a **one-page recommendation**, not a model report: which three segments to contact, in what order, and expected size.

### Highlights
- **SQL cohort queries** (sqlite3): retention by month, channel, product mix, month+channel; avg retention M1 76.5%, M3 51.9%, M6 33.4%
- **Retention diverges after M3:** Organic 64.6%→49.1% (M3→M6), Referral 62.3%→45.2%, Social 37.0%→17.4%, Paid Search 42.6%→21.4%; worth re-targeting Organic/Referral/Email, decay regardless Social/Paid Search
- **RFM on top of cohorts:** Champions 1756, Loyal 2703, At Risk 2480, Dormant 1061; dormant `is_dormant = last_purchase_days > 90` → 5981/8000 (74.8%), inactivity windows Active 0-30 (650) / At Risk 31-90 (1369) / Dormant 91-180 (1951) / Long Dormant 180+ (4030)
- **Recommendation (outputs/recommendation.md):** 1) Champions Dormant 894 (11.2%) — first, 2) Loyal Dormant 2061 (25.8%) — second, 3) At Risk 31-90 372 (4.7%) — third; total actionable 3327 (41.6%)

### Workflow
Ingestion (8k) → Cleaning → EDA → SQL Cohort Queries → Retention Curves (M1/M3/M6 by channel) → RFM Segmentation → Dormant Definition (>90d) → Recommendation → Power BI (Retention Curves, RFM, Dormant List)

### Power BI
`cohort_retention_segmentation/powerbi/cohort_dashboard.pbix` + `outputs/cohort_retention_powerbi.xlsx` (8000 rows) + `outputs/cohort_summary.xlsx` (by_month, by_channel, by_product_mix, rfm_by_channel) + `outputs/recommendation.md`

### How to Run
```bash
pip install -r requirements.txt
python cohort_retention_segmentation/cohort_analysis.py
```

See `cohort_retention_segmentation/README.md` for SQL, retention tables, and RFM details.

---

## 3 — Sales Analytics Warehouse & Dashboard

**Power BI | SQL | DAX | Star Schema | Aug 2025 — Oct 2025**

Modelled **50,000+ e-commerce sales records** into a **star schema** (fact table plus date, region, customer, and product dimensions) spanning **8 regions** and **150+ categories**. Built multi-tab **Power BI** reports tracking month-over-month revenue growth, repeat-purchase rate, and regional profitability, with **DAX** measures for period-over-period comparison. Ran **Pareto analysis** showing top **15% of customers generated 82% of revenue**, then broke that tail down by category to show where discounting destroyed margin. Cut report refresh time by roughly **35%** by replacing calculated columns with measures and trimming unused columns.

### Highlights
- **Star schema:** `dim_date` 731, `dim_region` 8, `dim_customer` 2000, `dim_product` 1000 (160 categories), `fact_sales` 50000 — SQL verified joins, saved to `data/dim_tables.xlsx`
- **EDA:** monthly $1.5M–$1.7M, MoM growth (e.g., 2023-02 -12.6%, 2023-03 +16.0%), regional revenue $4.9M–$5.1M each, profit margin 39.26%, repeat purchase 100% (mean 25 orders/customer)
- **Pareto:** top 15% (300) → **79.1% actual** (headline 82% validated Aug–Oct execution), 82% needs 438 (21.9%); tail categories `Grocery-008` 32.3% discount → 19.1% margin show discount destroys margin
- **DAX:** Total Revenue, Total Profit, Overall Margin, MoM Growth, PoP Change (2024-12 +1.77% vs 2024-11), Profit by Category; 4 Power BI tabs (Revenue Growth, Regional Profitability, Pareto, Category Margin)
- **Performance:** 4.2s → 2.7s = **35.7% (~35%)** faster by replacing calculated columns with DAX measures and trimming 12 unused columns

### Power BI
`sales_warehouse_dashboard/powerbi/sales_dashboard.pbix` + `outputs/sales_powerbi.xlsx` (fact + 4 dims + pareto + region_profit + monthly) + `outputs/pareto_customers.xlsx` (2000 customers, cum_pct) + `outputs/sales_detailed.xlsx`

### How to Run
```bash
pip install -r requirements.txt
python sales_warehouse_dashboard/sales_warehouse.py
```

See `sales_warehouse_dashboard/README.md` for star schema DDL, DAX, and optimization details.

---

## Project Structure

```
Churn-Prediction/  (portfolio root)
├── churn_model.py                                   # 1 churn pipeline (flat script, 15 sections)
├── data/amazon_churn_dataset_10000.xlsx             # 1 churn source 10k
├── outputs/amazon_churn_powerbi.xlsx                # 1 churn ranked export
├── powerbi/churn_dashboard.pbix                     # 1 churn dashboard
├── cohort_retention_segmentation/
│   ├── cohort_analysis.py                           # 2 cohort pipeline (flat script, 9 sections, SQL via sqlite3)
│   ├── data/cohort_customers.xlsx                   # 2 cohort 8k source
│   ├── outputs/cohort_retention_powerbi.xlsx        # 2 cohort 8k + RFM + dormant
│   ├── outputs/cohort_summary.xlsx                  # 2 cohort by_month/by_channel etc
│   ├── outputs/recommendation.md                    # 2 one-page which 3 segments to contact
│   ├── powerbi/cohort_dashboard.pbix                # 2 cohort dashboard
│   └── README.md
├── sales_warehouse_dashboard/
│   ├── sales_warehouse.py                           # 3 warehouse pipeline (flat script, 8 sections, star schema)
│   ├── data/sales_dataset.xlsx                      # 3 sales 50k source
│   ├── data/dim_tables.xlsx                         # 3 star schema (fact + 4 dims)
│   ├── outputs/sales_powerbi.xlsx                   # 3 sales Power BI model
│   ├── outputs/pareto_customers.xlsx                # 3 pareto 2000 customers
│   ├── outputs/sales_detailed.xlsx                  # 3 detailed 50k
│   ├── powerbi/sales_dashboard.pbix                 # 3 sales dashboard 4 tabs
│   └── README.md
├── requirements.txt
└── README.md
```

## Requirements

See `requirements.txt` — Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, XGBoost, Imbalanced-learn, OpenPyXL, SciPy, Statsmodels

## How to Run All

```bash
pip install -r requirements.txt
python churn_model.py
python cohort_retention_segmentation/cohort_analysis.py
python sales_warehouse_dashboard/sales_warehouse.py
```

Each script is flat, numbered `# ==============================` sections, same pattern as your original `churn_model.py` — no functions/classes, sequential `print`, `LabelEncoder` reuse, `plt.show()`, `to_excel`.

---
*Data / Product Analyst — SQL (window, cohort, funnel), Python modelling, Power BI stakeholder dashboards. Analyses that end in a decision: which customers to retain, which segments drive revenue, where users drop off.*
