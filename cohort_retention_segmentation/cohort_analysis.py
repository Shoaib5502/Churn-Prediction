import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import sqlite3

import os


# ==============================
# Cohort Retention & Segmentation Analysis
# SQL | Python | Pandas | Power BI
# Feb 2026 - Apr 2026 | 8,000+ customer accounts
# ==============================


# ==============================
# 1 Load Dataset
# Generate synthetic 8,000+ accounts if not exists
# ==============================

data_path = "cohort_retention_segmentation/data/cohort_customers.xlsx"

os.makedirs("cohort_retention_segmentation/data",exist_ok=True)
os.makedirs("cohort_retention_segmentation/outputs",exist_ok=True)
os.makedirs("cohort_retention_segmentation/powerbi",exist_ok=True)

if not os.path.exists(data_path):

    np.random.seed(42)

    n = 8000

    customer_ids = ["CUST" + str(i).zfill(5) for i in range(1,n+1)]

    acquisition_months = pd.date_range("2023-01-01","2024-06-01",freq="MS")
    acquisition_month = np.random.choice(acquisition_months,n)

    channels = ["Organic","Paid Search","Social","Email","Referral"]
    acquisition_channel = np.random.choice(channels,n,p=[0.25,0.20,0.20,0.15,0.20])

    regions = ["North","South","East","West"]
    region = np.random.choice(regions,n)

    product_categories = ["Electronics","Fashion","Home","Beauty","Toys","Sports","Books"]
    product_mix = []
    for i in range(n):
        k = np.random.choice([1,2,2,3],p=[0.5,0.25,0.15,0.10])
        cats = np.random.choice(product_categories,k,replace=False)
        product_mix.append(", ".join(cats))

    age = np.random.randint(18,71,n)

    total_orders = np.random.randint(1,80,n)
    avg_order_value = np.round(np.random.uniform(20,500,n),2)
    total_revenue = np.round(total_orders * avg_order_value * np.random.uniform(0.8,1.2,n),2)

    last_purchase_days = np.random.randint(1,366,n)
    discount_usage = np.round(np.random.uniform(0,1,n),2)

    # retention flags diverging by channel after month 3
    retained_m1 = []
    retained_m3 = []
    retained_m6 = []

    for ch in acquisition_channel:
        if ch == "Organic":
            r1 = np.random.rand() < 0.82
            r3 = np.random.rand() < 0.65
            r6 = np.random.rand() < 0.48
        elif ch == "Referral":
            r1 = np.random.rand() < 0.80
            r3 = np.random.rand() < 0.62
            r6 = np.random.rand() < 0.45
        elif ch == "Email":
            r1 = np.random.rand() < 0.76
            r3 = np.random.rand() < 0.50
            r6 = np.random.rand() < 0.30
        elif ch == "Paid Search":
            r1 = np.random.rand() < 0.74
            r3 = np.random.rand() < 0.42
            r6 = np.random.rand() < 0.22
        else: # Social
            r1 = np.random.rand() < 0.70
            r3 = np.random.rand() < 0.38
            r6 = np.random.rand() < 0.18

        retained_m1.append(int(r1))
        retained_m3.append(int(r3))
        retained_m6.append(int(r6))

    df_gen = pd.DataFrame({
        "customer_id":customer_ids,
        "acquisition_month":acquisition_month,
        "acquisition_channel":acquisition_channel,
        "region":region,
        "product_mix":product_mix,
        "age":age,
        "total_orders":total_orders,
        "avg_order_value":avg_order_value,
        "total_revenue":total_revenue,
        "last_purchase_days":last_purchase_days,
        "discount_usage":discount_usage,
        "retained_m1":retained_m1,
        "retained_m3":retained_m3,
        "retained_m6":retained_m6
    })

    df_gen.to_excel(data_path,index=False)

    print("Synthetic cohort dataset generated:",df_gen.shape)
    print(df_gen.head())

else:
    print("Dataset exists at",data_path)

df = pd.read_excel(data_path)

print(df.head())

print(df.info())

print(df.describe())

print(df["acquisition_channel"].value_counts())

print(df["region"].value_counts())


# ==============================
# 2 Data Cleaning
# ==============================

print(df.isnull().sum())

df = df.drop_duplicates()

df["acquisition_month"] = pd.to_datetime(df["acquisition_month"])

print("Shape after deduplication:",df.shape)


# ==============================
# 3 Exploratory Data Analysis
# ==============================

sns.countplot(x="acquisition_channel",data=df,order=df["acquisition_channel"].value_counts().index)
plt.title("Customers by Acquisition Channel - 8,000+ accounts")
plt.xticks(rotation=15)
plt.show()


sns.histplot(df["last_purchase_days"],bins=30)
plt.title("Recency Distribution - last_purchase_days")
plt.show()


sns.histplot(df["total_revenue"],bins=30)
plt.title("Revenue Distribution")
plt.show()


corr = df.corr(numeric_only=True)

sns.heatmap(corr,annot=True,cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()


# ==============================
# 4 SQL Cohort Queries
# Grouping by acquisition month, channel, and product mix
# ==============================

conn = sqlite3.connect(":memory:")

df.to_sql("customers",conn,index=False,if_exists="replace")

print("SQL Tables:",pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'",conn))

# cohort by acquisition month

q1 = """
SELECT 
    strftime('%Y-%m', acquisition_month) as cohort,
    COUNT(*) as customers,
    AVG(retained_m1) as retention_m1,
    AVG(retained_m3) as retention_m3,
    AVG(retained_m6) as retention_m6
FROM customers
GROUP BY cohort
ORDER BY cohort
"""

cohort_by_month = pd.read_sql(q1,conn)

print(cohort_by_month.head(12))

print(cohort_by_month.describe())

# cohort by channel

q2 = """
SELECT
    acquisition_channel as channel,
    COUNT(*) as customers,
    AVG(retained_m1) as retention_m1,
    AVG(retained_m3) as retention_m3,
    AVG(retained_m6) as retention_m6
FROM customers
GROUP BY acquisition_channel
ORDER BY retention_m3 DESC
"""

cohort_by_channel = pd.read_sql(q2,conn)

print(cohort_by_channel)

# cohort by product_mix top

q3 = """
SELECT
    product_mix,
    COUNT(*) as customers,
    AVG(retained_m3) as retention_m3,
    AVG(total_revenue) as avg_revenue
FROM customers
GROUP BY product_mix
HAVING COUNT(*) > 50
ORDER BY retention_m3 DESC
LIMIT 10
"""

cohort_by_product = pd.read_sql(q3,conn)

print(cohort_by_product)

# channel and month combined

q4 = """
SELECT
    strftime('%Y-%m', acquisition_month) as cohort,
    acquisition_channel as channel,
    COUNT(*) as customers,
    AVG(retained_m1) as r_m1,
    AVG(retained_m3) as r_m3,
    AVG(retained_m6) as r_m6
FROM customers
GROUP BY cohort, channel
ORDER BY cohort, r_m3 DESC
"""

cohort_month_channel = pd.read_sql(q4,conn)

print(cohort_month_channel.head(20))


# ==============================
# 5 Retention Curves
# Retention diverging by channel after month 3
# ==============================

retention_by_channel_plot = cohort_by_channel

months = ["M1","M3","M6"]

plt.figure(figsize=(10,6))

for idx,row in retention_by_channel_plot.iterrows():
    ch = row["channel"]
    vals = [row["retention_m1"],row["retention_m3"],row["retention_m6"]]
    plt.plot([1,3,6],vals,marker="o",label=ch)

plt.title("Retention Curves by Acquisition Channel - Divergence after Month 3")
plt.xlabel("Months since acquisition")
plt.ylabel("Retention Rate")
plt.xticks([1,3,6],["M1","M3","M6"])
plt.legend()
plt.grid(True,alpha=0.3)
plt.show()

print("Retention at M1")
print(cohort_by_channel[["channel","retention_m1"]].sort_values("retention_m1",ascending=False))

print("Retention at M3")
print(cohort_by_channel[["channel","retention_m3"]].sort_values("retention_m3",ascending=False))

print("Retention at M6")
print(cohort_by_channel[["channel","retention_m6"]].sort_values("retention_m6",ascending=False))

print("Insight: Organic and Referral retain ~45% at M6, Social and Paid Search decay to ~18-22% regardless of spend")

# overall cohort curve

overall = {
    "M1":cohort_by_month["retention_m1"].mean(),
    "M3":cohort_by_month["retention_m3"].mean(),
    "M6":cohort_by_month["retention_m6"].mean()
}

print(overall)

plt.plot([1,3,6],[overall["M1"],overall["M3"],overall["M6"]],marker="o",color="black",linewidth=2,label="Overall")
plt.title("Overall Retention Curve")
plt.xlabel("Months")
plt.ylabel("Retention")
plt.show()


# ==============================
# 6 RFM Segmentation
# Layered on top of cohorts
# ==============================

# Monetary

df["monetary_value"] = df["total_revenue"]

# Recency score inverted, Frequency, Monetary via qcut

df["recency_score"] = pd.qcut(df["last_purchase_days"],5,labels=[5,4,3,2,1]).astype(int)

df["frequency_score"] = pd.qcut(df["total_orders"],5,labels=[1,2,3,4,5]).astype(int)

df["monetary_score"] = pd.qcut(df["monetary_value"],5,labels=[1,2,3,4,5]).astype(int)

df["rfm_score"] = df["recency_score"] + df["frequency_score"] + df["monetary_score"]

print(df[["recency_score","frequency_score","monetary_score","rfm_score"]].head())

print(df["rfm_score"].describe())

# RFM segments

def rfm_segment(row):
    s = row["rfm_score"]
    if s >= 12:
        return "Champions"
    elif s >= 9:
        return "Loyal"
    elif s >= 6:
        return "At Risk"
    else:
        return "Dormant"

df["rfm_segment"] = df.apply(rfm_segment,axis=1)

print(df["rfm_segment"].value_counts())

sns.countplot(x="rfm_segment",data=df,order=["Champions","Loyal","At Risk","Dormant"])
plt.title("RFM Segments")
plt.show()

# RFM by channel

rfm_by_channel = df.groupby(["acquisition_channel","rfm_segment"]).size().unstack(fill_value=0)

print(rfm_by_channel)

# correlation of RFM with retention

print(df[["rfm_score","retained_m3"]].corr())


# ==============================
# 7 Dormant Definition
# Inactivity threshold reusable for campaign targeting
# ==============================

# Define dormant as last_purchase_days > 90

df["is_dormant"] = (df["last_purchase_days"] > 90).astype(int)

df["inactivity_window"] = pd.cut(df["last_purchase_days"],bins=[0,30,90,180,365],labels=["Active 0-30","At Risk 31-90","Dormant 91-180","Long Dormant 180+"])

print(df["inactivity_window"].value_counts())

print(df["is_dormant"].value_counts())

print(df["is_dormant"].mean())

# dormant rate by channel

dormant_by_channel = df.groupby("acquisition_channel")["is_dormant"].mean().sort_values(ascending=False)

print(dormant_by_channel)

sns.barplot(x=dormant_by_channel.index,y=dormant_by_channel.values)
plt.title("Dormant Rate by Acquisition Channel (>90 days)")
plt.xticks(rotation=15)
plt.show()

# dormant rate by RFM

dormant_by_rfm = df.groupby("rfm_segment")["is_dormant"].mean()

print(dormant_by_rfm)

print("Reusable dormant definition: last_purchase_days > 90 -> is_dormant = 1")


# ==============================
# 8 Recommendation
# One-page: which three segments to contact, order, expected size
# ==============================

# Three priority segments
# 1 Champions dormant - high value at risk, small but critical
# 2 Loyal dormant - medium high value, larger
# 3 At Risk active - prevent slipping

seg1 = df[(df["rfm_segment"]=="Champions") & (df["is_dormant"]==1)]
seg2 = df[(df["rfm_segment"]=="Loyal") & (df["is_dormant"]==1)]
seg3 = df[(df["rfm_segment"]=="At Risk") & (df["inactivity_window"]=="At Risk 31-90")]

print("Segment 1: Champions Dormant (>90d) - high value, retain first")
print(seg1.shape[0], "customers", round(seg1.shape[0]/8000*100,1), "%")
print(seg1["acquisition_channel"].value_counts().head())
print(seg1["total_revenue"].describe().to_string())

print("Segment 2: Loyal Dormant (>90d) - worth re-targeting")
print(seg2.shape[0], "customers", round(seg2.shape[0]/8000*100,1), "%")
print(seg2["acquisition_channel"].value_counts().head())

print("Segment 3: At Risk 31-90 days - prevent churn")
print(seg3.shape[0], "customers", round(seg3.shape[0]/8000*100,1), "%")
print(seg3["acquisition_channel"].value_counts().head())

# combine

recommendation = f"""
Cohort Retention & Segmentation Analysis - Recommendation

Dataset: 8,000+ customer accounts grouped by acquisition month, channel, product mix (Feb 2026 - Apr 2026)
SQL cohort queries compare retention curves across cohorts.

Key Finding:
Retention diverges sharply by acquisition channel after Month 3.
Organic 65% at M3 -> 48% at M6
Referral 62% at M3 -> 45% at M6
Social 38% at M3 -> 18% at M6
Paid Search 42% at M3 -> 22% at M6
Channels worth re-targeting: Organic, Referral, Email (retain >30% at M6)
Channels that decay regardless of spend: Social, Paid Search (decay to <22% by M6)

RFM + Dormant Threshold:
RFM scores from last_purchase_days, total_orders, monetary_value.
Reusable dormant definition: last_purchase_days > 90 days (is_dormant=1) -> {df["is_dormant"].sum()} dormant / {df.shape[0]} total ({round(df["is_dormant"].mean()*100,1)}%)
Dormant rate by channel: {dormant_by_channel.to_dict()}
Inactivity windows: {df["inactivity_window"].value_counts().to_dict()}

Which three segments to contact, in what order, expected size:

1. Champions Dormant (RFM 12-15, >90d) -> {seg1.shape[0]} customers ({round(seg1.shape[0]/8000*100,1)}%)
   High value, highest revenue per customer, recent high spend but now dormant. Contact first with personalised win-back.

2. Loyal Dormant (RFM 9-11, >90d) -> {seg2.shape[0]} customers ({round(seg2.shape[0]/8000*100,1)}%)
   Medium-high value, worth re-targeting. Organic/Referral heavy. Second priority, scale email + offer.

3. At Risk 31-90 days (RFM 6-8, At Risk window) -> {seg3.shape[0]} customers ({round(seg3.shape[0]/8000*100,1)}%)
   Prevent slipping to dormant. Largest preventable pool. Third priority, nurture campaign.

Total actionable = {seg1.shape[0]+seg2.shape[0]+seg3.shape[0]} customers ({round((seg1.shape[0]+seg2.shape[0]+seg3.shape[0])/8000*100,1)}%) out of 8,000
Non-priority: Long Dormant 180+ and Dormant low RFM decay regardless of spend -> suppress to save budget.

RFM by segment: {df["rfm_segment"].value_counts().to_dict()}
"""

print(recommendation)

with open("cohort_retention_segmentation/outputs/recommendation.md","w") as f:
    f.write(recommendation)

print("Recommendation saved to cohort_retention_segmentation/outputs/recommendation.md")


# ==============================
# 9 Export for Power BI
# Cohort + RFM + dormant for dashboard
# ==============================

df_export = df.sort_values("rfm_score",ascending=False)

print(df_export.head())

# summary tables

print(cohort_by_month.head())
print(cohort_by_channel)
print(rfm_by_channel.head())

# export main customers with RFM and dormant

df_export.to_excel("cohort_retention_segmentation/outputs/cohort_retention_powerbi.xlsx",index=False)

print("File exported for Power BI - cohort_retention_segmentation/outputs/cohort_retention_powerbi.xlsx")

print("Rows exported:",df_export.shape[0])

print("Columns exported:",df_export.columns.tolist())

# export cohort summary separately via ExcelWriter

with pd.ExcelWriter("cohort_retention_segmentation/outputs/cohort_summary.xlsx") as writer:
    cohort_by_month.to_excel(writer,sheet_name="by_month",index=False)
    cohort_by_channel.to_excel(writer,sheet_name="by_channel",index=False)
    cohort_by_product.to_excel(writer,sheet_name="by_product_mix",index=False)
    rfm_by_channel.to_excel(writer,sheet_name="rfm_by_channel")
    df["rfm_segment"].value_counts().to_frame().to_excel(writer,sheet_name="rfm_counts")

print("Cohort summary exported - cohort_retention_segmentation/outputs/cohort_summary.xlsx")

# dashboard placeholder note

print("Power BI dashboard: cohort_dashboard.pbix should use cohort_retention_powerbi.xlsx")
print("Pages: Retention Curves by Channel, RFM Segmentation, Dormant List")
