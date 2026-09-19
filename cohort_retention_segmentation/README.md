# Cohort Retention & Segmentation Analysis

**SQL | Python | Pandas | Power BI**
**Feb 2026 — Apr 2026**

Analysed **8,000+ customer accounts** with SQL cohort queries, grouping by acquisition month, channel, and product mix to compare retention curves across cohorts. Layered RFM segmentation on top to define a reusable dormant-customer definition for campaign targeting. Output is a one-page recommendation, not a model report: which three segments to contact, in what order, and expected size.

---

## Overview

This project answers: which acquisition cohorts retain, which decay after month 3, and which customers are worth re-targeting. It uses SQL for cohort grouping and Python for RFM and retention-curve analysis.

## Dataset

- **Source:** `data/cohort_customers.xlsx` — 8,000 customers (synthetic, seeded 42) spanning acquisition months 2023-01 to 2024-06
- **Columns:** `customer_id`, `acquisition_month`, `acquisition_channel` (Organic, Paid Search, Social, Email, Referral), `region`, `product_mix`, `age`, `total_orders`, `avg_order_value`, `total_revenue`, `last_purchase_days`, `discount_usage`, `retained_m1`, `retained_m3`, `retained_m6`
- **Engineered:** `monetary_value`, `recency_score`, `frequency_score`, `monetary_score`, `rfm_score`, `rfm_segment` (Champions/Loyal/At Risk/Dormant), `is_dormant` (>90 days), `inactivity_window` (Active 0-30, At Risk 31-90, Dormant 91-180, Long Dormant 180+)
- **Target analysis:** retention at M1, M3, M6 by cohort

## Tools Used

**SQL** (window and cohort queries via `sqlite3`), **Python**, **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**, **Power BI** (DAX, cohort visuals)

**Analytics:** Cohort Analysis, Retention Curves, RFM Segmentation, Inactivity Thresholding, Exploratory Data Analysis

## Workflow

    |
Data Generation / Ingestion (Excel, 8k accounts)
    |
Data Cleaning (null check, drop_duplicates, acquisition_month to datetime)
    |
Exploratory Data Analysis (channel distribution, recency, revenue, correlation)
    |
SQL Cohort Queries (group by acquisition month, channel, product mix)
    |
Retention Curves (M1, M3, M6 by channel — divergence after M3)
    |
RFM Segmentation (recency/frequency/monetary qcut, rfm_score)
    |
Dormant Definition (last_purchase_days > 90, reusable for campaigns)
    |
Recommendation (three segments, order, expected size)
    |
Dashboard Visualization (Power BI)

## SQL Cohort Queries

Executed in `sqlite3` in-memory (`customers` table):

```sql
-- retention by acquisition month
SELECT strftime('%Y-%m', acquisition_month) as cohort,
       COUNT(*) as customers,
       AVG(retained_m1) as retention_m1,
       AVG(retained_m3) as retention_m3,
       AVG(retained_m6) as retention_m6
FROM customers GROUP BY cohort ORDER BY cohort;

-- retention by channel
SELECT acquisition_channel as channel,
       COUNT(*) as customers,
       AVG(retained_m1) as retention_m1,
       AVG(retained_m3) as retention_m3,
       AVG(retained_m6) as retention_m6
FROM customers GROUP BY acquisition_channel ORDER BY retention_m3 DESC;

-- channel + month combined
SELECT strftime('%Y-%m', acquisition_month) as cohort,
       acquisition_channel as channel,
       COUNT(*) as customers,
       AVG(retained_m3) as r_m3
FROM customers GROUP BY cohort, channel ORDER BY cohort, r_m3 DESC;
```

## Key Findings — Resume Aligned

- **Retention diverges sharply by acquisition channel after month 3:**
  - Organic 64.6% at M3 → 49.2% at M6
  - Referral 62.3% at M3 → 45.2% at M6
  - Email 49.6% at M3 → 29.3% at M6
  - Paid Search 42.6% at M3 → 21.4% at M6
  - Social 37.0% at M3 → 17.4% at M6
- **Channels worth re-targeting:** Organic, Referral, Email (retain >30% at M6)
- **Channels that decay regardless of spend:** Social, Paid Search (decay to <22% by M6, suppress budget)

## RFM + Dormant Threshold

- **RFM scores:** `recency_score` from `last_purchase_days` (qcut 5 inverted), `frequency_score` from `total_orders`, `monetary_score` from `total_revenue`; `rfm_score = sum`
- **Segments:** Champions (12-15) 1756, Loyal (9-11) 2703, At Risk (6-8) 2480, Dormant (3-5) 1061
- **Reusable dormant definition:** `is_dormant = last_purchase_days > 90` → 5,981 dormant / 8,000 (74.8%)
- **Inactivity windows:** Active 0-30 (650), At Risk 31-90 (1369), Dormant 91-180 (1951), Long Dormant 180+ (4030)
- Dormant rate by channel highest in Social (76%) and Organic (75%), lowest Email (72.5%) — definition reusable for campaign targeting

## Recommendation — Which Three Segments to Contact

See `outputs/recommendation.md` (one-page):

**1. Champions Dormant (RFM 12-15, >90d) → 894 customers (11.2%)**
High value, highest revenue per customer (mean $22,881). Contact first with personalised win-back.

**2. Loyal Dormant (RFM 9-11, >90d) → 2,061 customers (25.8%)**
Medium-high value, worth re-targeting. Organic/Referral heavy. Second priority, scale email + offer.

**3. At Risk 31-90 days (RFM 6-8, At Risk window) → 372 customers (4.7%)**
Prevent slipping to dormant. Third priority, nurture campaign.

Total actionable = 3,327 customers (41.6%) out of 8,000. Long Dormant 180+ and low RFM decay regardless — suppress to save budget.

## Power BI Dashboard

**File:** `powerbi/cohort_dashboard.pbix` and `outputs/cohort_retention_powerbi.xlsx`

- **Pages:** Retention Curves by Channel (M1/M3/M6), RFM Segmentation (Champions/Loyal/At Risk/Dormant), Dormant List (ranked by `rfm_score` + `inactivity_window`)
- **Exports:** `cohort_retention_powerbi.xlsx` (8000 rows, 22 cols), `cohort_summary.xlsx` (by_month, by_channel, by_product_mix, rfm_by_channel sheets)

## How to Run

```bash
pip install -r ../../requirements.txt
python cohort_retention_segmentation/cohort_analysis.py
```

Outputs:
- Console: cohort tables, retention curves, RFM counts, dormant rates, recommendation
- Files: `outputs/cohort_retention_powerbi.xlsx`, `outputs/cohort_summary.xlsx`, `outputs/recommendation.md`

## Project Structure

```
cohort_retention_segmentation/
├── data/
│   └── cohort_customers.xlsx              # 8k accounts source
├── cohort_analysis.py                     # flat script, numbered sections (SQL + Python)
├── outputs/
│   ├── cohort_retention_powerbi.xlsx      # 8000 rows + RFM + dormant for Power BI
│   ├── cohort_summary.xlsx                # by_month, by_channel, by_product_mix
│   └── recommendation.md                  # one-page which 3 segments to contact
├── powerbi/
│   └── cohort_dashboard.pbix              # retention curves + RFM + dormant list
└── README.md
```

## Requirements

See `../../requirements.txt` — Pandas, NumPy, Matplotlib, Seaborn, SciPy, openpyxl

---
*Feb 2026 — Apr 2026 | SQL cohort queries, Python RFM, Power BI stakeholder one-pager*
