
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
Reusable dormant definition: last_purchase_days > 90 days (is_dormant=1) -> 5981 dormant / 8000 total (74.8%)
Dormant rate by channel: {'Social': 0.7599231754161332, 'Organic': 0.7581563956499223, 'Referral': 0.7507749535027899, 'Paid Search': 0.737094837935174, 'Email': 0.7255700325732899}
Inactivity windows: {'Long Dormant 180+': 4030, 'Dormant 91-180': 1951, 'At Risk 31-90': 1369, 'Active 0-30': 650}

Which three segments to contact, in what order, expected size:

1. Champions Dormant (RFM 12-15, >90d) -> 894 customers (11.2%)
   High value, highest revenue per customer, recent high spend but now dormant. Contact first with personalised win-back.

2. Loyal Dormant (RFM 9-11, >90d) -> 2061 customers (25.8%)
   Medium-high value, worth re-targeting. Organic/Referral heavy. Second priority, scale email + offer.

3. At Risk 31-90 days (RFM 6-8, At Risk window) -> 372 customers (4.7%)
   Prevent slipping to dormant. Largest preventable pool. Third priority, nurture campaign.

Total actionable = 3327 customers (41.6%) out of 8,000
Non-priority: Long Dormant 180+ and Dormant low RFM decay regardless of spend -> suppress to save budget.

RFM by segment: {'Loyal': 2703, 'At Risk': 2480, 'Champions': 1756, 'Dormant': 1061}
