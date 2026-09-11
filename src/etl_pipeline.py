"""
etl_pipeline.py
---------------
Automated ETL & Star Schema Data Modeling Pipeline.

Transforms raw transaction files into analytical Dimension & Fact tables:
1. Dim_Customers.csv
2. Dim_Plans.csv
3. Dim_Date.csv
4. Dim_ChurnReason.csv
5. Fact_Subscriptions.csv
6. Fact_Customer_Health_Score.csv
7. Fact_Monthly_Cohorts.csv

Also loads the cleaned Star Schema into an SQLite analytical database
`data/processed/saas_churn_intelligence.db` for zero-setup SQL analytics.
"""

import os
import csv
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

DB_PATH = os.path.join(PROCESSED_DIR, "saas_churn_intelligence.db")

print("[*] Initiating Stage 1 ETL Data Cleaning & Transformation Pipeline...")

# 1. READ RAW FILES
def read_csv_dict(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

raw_cust = read_csv_dict(os.path.join(RAW_DIR, "raw_customers.csv"))
raw_subs = read_csv_dict(os.path.join(RAW_DIR, "raw_subscriptions.csv"))
raw_usage = {r["customer_id"]: r for r in read_csv_dict(os.path.join(RAW_DIR, "raw_usage_events.csv"))}
raw_tickets = {r["customer_id"]: r for r in read_csv_dict(os.path.join(RAW_DIR, "raw_support_tickets.csv"))}

# 2. STANDARDIZATION & CLEANING
def clean_channel(ch):
    ch = ch.strip()
    mapping = {
        "outbound_sales": "Outbound Sales",
        "paid ads": "Paid Ads",
        "organic search": "Organic Search",
        "referral": "Referral",
        "email campaign": "Email Campaign",
        "direct": "Direct",
        "social media": "Social Media"
    }
    return mapping.get(ch.lower(), ch.title())

# 3. BUILD DIM_CUSTOMERS
dim_customers = []
customer_signup_map = {}

for r in raw_cust:
    cid = r["customer_id"]
    signup_dt = datetime.strptime(r["signup_date"], "%Y-%m-%d")
    cohort_month = signup_dt.strftime("%Y-%m")
    customer_signup_map[cid] = signup_dt
    
    dim_customers.append({
        "customer_id": cid,
        "signup_date": r["signup_date"],
        "cohort_month": cohort_month,
        "acquisition_channel": clean_channel(r["acquisition_channel"]),
        "country": r["country"].strip(),
        "customer_segment": r["customer_segment"].strip()
    })

# 4. BUILD DIM_PLANS
dim_plans = [
    {"plan_id": "PLAN-01", "plan_name": "Starter", "tier_level": 1, "base_monthly_price": 49.00, "target_segment": "SMB"},
    {"plan_id": "PLAN-02", "plan_name": "Professional", "tier_level": 2, "base_monthly_price": 149.00, "target_segment": "Mid-Market"},
    {"plan_id": "PLAN-03", "plan_name": "Enterprise", "tier_level": 3, "base_monthly_price": 499.00, "target_segment": "Enterprise"},
    {"plan_id": "PLAN-04", "plan_name": "Custom Enterprise", "tier_level": 4, "base_monthly_price": 1199.00, "target_segment": "Enterprise"}
]

# 5. BUILD DIM_CHURN_REASON
unique_reasons = sorted(list(set([r["churn_reason"].strip() for r in raw_subs if r["churn_reason"].strip()])))
dim_churn_reasons = []
for idx, reason in enumerate(unique_reasons):
    category = "Financial" if "Price" in reason or "Budget" in reason else (
        "Product" if "Feature" in reason else (
            "Service" if "Support" in reason else (
                "Competition" if "Competitor" in reason else (
                    "Adoption" if "Onboarding" in reason else "External"
                )
            )
        )
    )
    dim_churn_reasons.append({
        "reason_id": f"REA-{101 + idx}",
        "churn_reason": reason,
        "reason_category": category,
        "impact_tier": "High Risk" if category in ["Product", "Service"] else "Medium Risk"
    })

# 6. BUILD DIM_DATE (Calendar table for Power BI & SQL modeling)
dim_dates = []
cal_start = datetime(2024, 1, 1)
cal_end = datetime(2025, 12, 31)
curr = cal_start
while curr <= cal_end:
    dim_dates.append({
        "date_key": curr.strftime("%Y%m%d"),
        "full_date": curr.strftime("%Y-%m-%d"),
        "year": curr.year,
        "quarter": f"Q{(curr.month - 1) // 3 + 1}",
        "month": curr.month,
        "month_name": curr.strftime("%B"),
        "year_month": curr.strftime("%Y-%m"),
        "day_of_week": curr.strftime("%A"),
        "is_weekend": 1 if curr.weekday() >= 5 else 0
    })
    curr += timedelta(days=1)

# 7. BUILD FACT_SUBSCRIPTIONS
fact_subs = []
for r in raw_subs:
    cid = r["customer_id"]
    mrr = float(r["monthly_recurring_revenue"])
    start_dt = datetime.strptime(r["start_date"], "%Y-%m-%d")
    end_dt = datetime.strptime(r["end_date"], "%Y-%m-%d") if r["end_date"] else None
    
    tenure_days = (end_dt - start_dt).days if end_dt else (datetime(2025, 12, 31) - start_dt).days
    tenure_months = max(1, tenure_days // 30)
    customer_ltv = round(tenure_months * mrr, 2)
    is_churned = 1 if r["subscription_status"] == "Churned" else 0
    
    fact_subs.append({
        "subscription_id": r["subscription_id"],
        "customer_id": cid,
        "plan_name": r["plan_name"],
        "billing_cycle": r["billing_cycle"],
        "monthly_recurring_revenue": mrr,
        "annual_run_rate_arr": round(mrr * 12, 2),
        "start_date": r["start_date"],
        "end_date": r["end_date"] if r["end_date"] else "",
        "subscription_status": r["subscription_status"],
        "is_churned": is_churned,
        "churn_reason": r["churn_reason"],
        "tenure_months": tenure_months,
        "customer_lifetime_value_ltv": customer_ltv
    })

# 8. BUILD FACT_CUSTOMER_HEALTH_SCORE
fact_health = []
for cid, u in raw_usage.items():
    t = raw_tickets.get(cid, {})
    
    act_days = int(u["monthly_active_days"])
    adopt_pct = float(u["feature_adoption_rate_pct"])
    session_mins = float(u["avg_daily_session_mins"])
    tickets = int(t.get("total_tickets_logged", 0))
    res_hrs = float(t.get("avg_resolution_time_hrs", 0.0))
    escalations = int(t.get("escalated_tickets_count", 0))
    csat = float(t.get("latest_csat_score")) if t.get("latest_csat_score") else 3.5
    
    # Customer Health Score (0 - 100)
    # Higher is healthier
    usage_component = (act_days / 30.0) * 40.0 + (adopt_pct / 100.0) * 30.0
    support_penalty = min(25.0, (tickets * 4.0) + (escalations * 10.0) + (res_hrs / 8.0))
    csat_bonus = (csat / 5.0) * 30.0
    
    health_score = max(5.0, min(100.0, round(usage_component + csat_bonus - support_penalty, 1)))
    
    if health_score >= 70.0:
        risk_segment = "Low Risk (Healthy)"
    elif health_score >= 45.0:
        risk_segment = "Medium Risk (Warning)"
    else:
        risk_segment = "High Risk (Critical)"
        
    fact_health.append({
        "customer_id": cid,
        "health_score": health_score,
        "risk_segment": risk_segment,
        "monthly_active_days": act_days,
        "feature_adoption_rate_pct": adopt_pct,
        "avg_daily_session_mins": session_mins,
        "api_calls_count": int(u["api_calls_count"]),
        "export_reports_count": int(u["export_reports_count"]),
        "total_tickets_logged": tickets,
        "avg_resolution_time_hrs": res_hrs,
        "escalated_tickets_count": escalations,
        "csat_score": csat
    })

# 9. BUILD FACT_MONTHLY_COHORTS
# Pre-calculate month-over-month cohort retention matrix for direct BI consumption
cohort_groups = defaultdict(list)
for sub in fact_subs:
    cid = sub["customer_id"]
    start_dt = datetime.strptime(sub["start_date"], "%Y-%m-%d")
    cohort = start_dt.strftime("%Y-%m")
    cohort_groups[cohort].append(sub)

fact_cohorts = []
all_months = sorted(list(set([d["year_month"] for d in dim_dates])))

for cohort_m, members in sorted(cohort_groups.items()):
    initial_users = len(members)
    initial_mrr = sum(m["monthly_recurring_revenue"] for m in members)
    
    cohort_start_dt = datetime.strptime(cohort_m + "-01", "%Y-%m-%d")
    
    for period in range(0, 13):
        # Calculate target month
        # Add 'period' months
        m_idx = (cohort_start_dt.year - 2024) * 12 + (cohort_start_dt.month - 1) + period
        if m_idx >= len(all_months):
            break
        act_month = all_months[m_idx]
        act_month_dt = datetime.strptime(act_month + "-01", "%Y-%m-%d")
        
        retained_users = 0
        retained_mrr = 0.0
        
        for m in members:
            s_dt = datetime.strptime(m["start_date"], "%Y-%m-%d")
            e_dt = datetime.strptime(m["end_date"], "%Y-%m-%d") if m["end_date"] else None
            
            # Was user active in this period?
            if s_dt <= act_month_dt:
                if e_dt is None or e_dt >= act_month_dt:
                    retained_users += 1
                    retained_mrr += m["monthly_recurring_revenue"]
                    
        user_retention_pct = round((retained_users / initial_users) * 100, 2) if initial_users > 0 else 0.0
        rev_retention_pct = round((retained_mrr / initial_mrr) * 100, 2) if initial_mrr > 0 else 0.0
        
        fact_cohorts.append({
            "cohort_month": cohort_m,
            "activity_month": act_month,
            "period_number": period,
            "starting_customers": initial_users,
            "retained_customers": retained_users,
            "customer_retention_rate_pct": user_retention_pct,
            "starting_mrr": round(initial_mrr, 2),
            "retained_mrr": round(retained_mrr, 2),
            "revenue_retention_rate_pct": rev_retention_pct
        })

# 10. WRITE ALL PROCESSED CSVS
tables = [
    ("Dim_Customers.csv", dim_customers),
    ("Dim_Plans.csv", dim_plans),
    ("Dim_ChurnReason.csv", dim_churn_reasons),
    ("Dim_Date.csv", dim_dates),
    ("Fact_Subscriptions.csv", fact_subs),
    ("Fact_Customer_Health_Score.csv", fact_health),
    ("Fact_Monthly_Cohorts.csv", fact_cohorts)
]

for filename, records in tables:
    filepath = os.path.join(PROCESSED_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        if records:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)
    print(f"[+] Exported {len(records)} rows to data/processed/{filename}")

# 11. LOAD INTO SQLITE DATABASE
print(f"[*] Creating analytical database at {DB_PATH}...")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def load_table(table_name, records):
    if not records:
        return
    cols = list(records[0].keys())
    col_defs = ", ".join([f'"{c}" TEXT' for c in cols])
    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    cursor.execute(f'CREATE TABLE "{table_name}" ({col_defs})')
    
    placeholders = ", ".join(["?" for _ in cols])
    rows = [[r[c] for c in cols] for r in records]
    cursor.executemany(f'INSERT INTO "{table_name}" VALUES ({placeholders})', rows)
    conn.commit()

for filename, records in tables:
    t_name = filename.replace(".csv", "")
    load_table(t_name, records)

conn.close()
print("[SUCCESS] Star Schema ETL Pipeline completed and SQLite DB populated successfully!")
