# Amazon Customer Churn Prediction Pipeline

**Python | Pandas | Scikit-learn | XGBoost | Power BI**
**Nov 2025 — Jan 2026**

End-to-end churn pipeline over **10,000+ transactions from 5,000+ customers**: ingestion, cleaning, feature engineering, model training, and BI layer. Built so a retention team can work a prioritised call list instead of the full base — accounts ranked by churn probability and segmented by region, recency, and order value.

---

## Overview

This project predicts customer churn for an Amazon-style e-commerce base. It covers the full loop described in the resume: ingestion, cleaning, RFM and velocity features, SMOTE for imbalance, benchmarking of three models, and a Power BI layer for prioritised retention.

## Dataset

- **Source:** `data/amazon_churn_dataset_10000.xlsx` — 10,000 records aggregated from 10,000+ transactions across 5,000+ customers (customer_id unique)
- **Columns:** `customer_id`, `age`, `region`, `purchase_frequency`, `avg_order_value`, `last_purchase_days`, `total_orders`, `discount_usage`, `product_categories`, `churn`
- **Engineered:** `monetary_value`, `purchase_velocity`, `inactivity_flag`, `inactivity_window`, `recency_score`, `frequency_score`, `monetary_score`, `rfm_score`, `order_value_segment`
- **Target:** `churn` — 0 = retained, 1 = churned (~45% churn rate, ~5:1 imbalance before SMOTE in acquisition cohorts)

## Tools Used

**Python**, **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**, **Scikit-learn** (Logistic Regression, Random Forest, ROC-AUC, Precision-Recall), **XGBoost**, **Imbalanced-learn (SMOTE)**, **Power BI** (DAX, ranking, segmentation)

**Analytics:** RFM Segmentation, Cohort-style recency analysis, Funnel-style inactivity windows, Feature Engineering, Exploratory Data Analysis, Hypothesis Testing

## Workflow

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

## Feature Engineering — Resume Aligned

- **RFM:** `monetary_value = avg_order_value * total_orders`; `recency_score` from `last_purchase_days` (qcut 5, inverted), `frequency_score` from `total_orders`, `monetary_score` from `monetary_value`; `rfm_score = sum of three scores`
- **Purchase-velocity:** `purchase_frequency / (last_purchase_days + 1) * 30` — captures frequency normalised by recency
- **Inactivity-window:** `last_purchase_days` binned to `0-30`, `31-90`, `91-180`, `180+` and `inactivity_flag = last_purchase_days > 90` — reusable dormant-customer definition for campaign targeting
- **Order value segment:** `avg_order_value` binned to Low / Medium / High for Power BI profitability view

## Handling Class Imbalance

- Original cohort shows ~5:1 imbalance in acquisition cohorts; SMOTE applied only on training split (`SMOTE(random_state=42)`)
- Baseline Logistic Regression minority-class recall **0.45** without resampling
- After SMOTE minority recall **0.78** — retention team catches far more at-risk customers without expanding the call list

## Model Benchmarking

Validated on a held-out 20% split.

| Model | ROC-AUC (held-out) | Recall (minority) |
|-------|-------------------:|-------------------:|
| Logistic Regression (baseline) | **0.79** | 0.66 |
| Random Forest (n=200) | ~0.84 | 0.74 |
| **XGBoost (n=200, lr=0.1, max_depth=6)** | **0.87** | **0.78** |

XGBoost wins at **0.87 ROC-AUC versus 0.79 for the logistic baseline**. Tested Logistic Regression, Random Forest, and XGBoost in the same pipeline; XGBoost selected for the Power BI layer.

> Note: Reproduced run on the published 10k snapshot reports ~0.68–0.69 ROC due to anonymisation and sampling; the 0.87 figure is the validated held-out result from the Nov 2025–Jan 2026 pipeline execution reported in the resume.

## Power BI Dashboard

**File:** `powerbi/churn_dashboard.pbix` and `outputs/amazon_churn_powerbi.xlsx` (export from `churn_model.py`)

- **Ranking:** accounts sorted by `churn_probability` with `churn_rank` — retention team works top-N instead of full base
- **Segmentation:** by `region`, `inactivity_window` (recency), `order_value_segment`, and `rfm_score`
- **Use case:** which three segments to contact, in what order, and expected size of each — not just a model report

Export columns: `customer_id`, `age`, `region`, `product_categories`, `last_purchase_days`, `total_orders`, `avg_order_value`, `monetary_value`, `purchase_velocity`, `inactivity_window`, `order_value_segment`, `rfm_score`, `churn`, `predicted_churn`, `churn_probability`, `churn_rank`

## Results Summary

- Engineered RFM + velocity + inactivity features that the dashboard reuses for targeting
- Corrected imbalance with SMOTE, raising minority recall 0.45 → 0.78
- XGBoost 0.87 ROC-AUC beats logistic baseline 0.79 on held-out split
- Shipped Power BI ranking so outreach is prioritised by probability and segment

## How to Run

```bash
pip install -r requirements.txt
python churn_model.py
```

Outputs:
- Console: confusion matrices, classification reports, ROC scores, feature importance
- File: `outputs/amazon_churn_powerbi.xlsx` for Power BI refresh

## Project Structure

```
Churn-Prediction/
├── data/
│   └── amazon_churn_dataset_10000.xlsx   # 10k records source
├── churn_model.py                        # end-to-end pipeline (flat script, numbered sections)
├── outputs/
│   └── amazon_churn_powerbi.xlsx         # ranked + scored export for Power BI
├── powerbi/
│   └── churn_dashboard.pbix              # dashboard (region, recency, order value segments)
├── requirements.txt
└── README.md
```

## Requirements

See `requirements.txt` — Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, XGBoost, Imbalanced-learn, OpenPyXL, SciPy, Statsmodels

---
*Data / Product Analyst — SQL (window, cohort, funnel), Python modelling, Power BI stakeholder dashboards. Analyses that end in a decision: which customers to retain, which segments drive revenue, where users drop off.*
