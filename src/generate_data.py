"""
generate_data.py
----------------
Enterprise-Grade Synthetic Data Generator for SaaS & E-Commerce Customer Churn
& Revenue Intelligence Dashboard.

Uses Python Standard Library (zero external dependencies required) to generate
12,500+ realistic customer records across 4 relational CSV tables:
1. data/raw/raw_customers.csv
2. data/raw/raw_subscriptions.csv
3. data/raw/raw_usage_events.csv
4. data/raw/raw_support_tickets.csv
"""

import os
import csv
import random
import math
from datetime import datetime, timedelta

# Set random seed for deterministic reproducibility
random.seed(42)

TOTAL_CUSTOMERS = 12500
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def exp_random(scale):
    # Inverse transform sampling for exponential distribution
    u = random.random()
    return -scale * math.log(1.0 - u)

print(f"[*] Starting synthetic data generation for {TOTAL_CUSTOMERS} enterprise customer accounts...")

# ==========================================
# 1. GENERATE CUSTOMERS
# ==========================================
customer_ids = [f"CUST-{100000 + i}" for i in range(TOTAL_CUSTOMERS)]

channels = ["Organic Search", "Paid Ads", "Referral", "Email Campaign", "Direct", "Social Media", "outbound_sales"]
channel_weights = [25, 28, 15, 12, 10, 6, 4]

countries = ["United States", "United Kingdom", "Germany", "Canada", "India", "Australia", "France", "Netherlands"]
country_weights = [42, 16, 12, 9, 8, 5, 4, 4]

segments = ["SMB", "Mid-Market", "Enterprise"]
segment_weights = [65, 25, 10]

customer_records = []

for cid in customer_ids:
    signup_dt = random_date(START_DATE, END_DATE - timedelta(days=30))
    channel = random.choices(channels, weights=channel_weights)[0]
    country = random.choices(countries, weights=country_weights)[0]
    segment = random.choices(segments, weights=segment_weights)[0]
    
    # Intentionally add occasional casing quirk for SQL/ETL cleaning demo
    if random.random() < 0.04:
        channel_str = channel.lower()
    else:
        channel_str = channel
        
    customer_records.append({
        "customer_id": cid,
        "signup_date": signup_dt.strftime("%Y-%m-%d"),
        "acquisition_channel": channel_str,
        "country": country,
        "customer_segment": segment
    })

customers_csv = os.path.join(OUTPUT_DIR, "raw_customers.csv")
with open(customers_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id", "signup_date", "acquisition_channel", "country", "customer_segment"])
    writer.writeheader()
    writer.writerows(customer_records)
print(f"[+] Saved {len(customer_records)} records to {customers_csv}")

# ==========================================
# 2. GENERATE SUBSCRIPTIONS, USAGE & TICKETS
# ==========================================
plan_types = ["Starter", "Professional", "Enterprise", "Custom Enterprise"]
billing_types = ["Monthly", "Annual"]

churn_reasons = [
    "High Price / Budget Cuts",
    "Missing Core Features",
    "Poor Customer Support Experience",
    "Switched to Competitor",
    "Difficult Onboarding / Low Adoption",
    "Business Closed / Downsized"
]

subscription_records = []
usage_records = []
ticket_records = []

active_count = 0
churned_count = 0
total_base_mrr = 0.0

for idx, cust in enumerate(customer_records):
    cid = cust["customer_id"]
    signup_dt = datetime.strptime(cust["signup_date"], "%Y-%m-%d")
    segment = cust["customer_segment"]
    channel = str(cust["acquisition_channel"]).title()
    
    # Plan assignment based on customer segment
    if segment == "SMB":
        plan = random.choices(plan_types[:2], weights=[75, 25])[0]
        billing = random.choices(billing_types, weights=[80, 20])[0]
    elif segment == "Mid-Market":
        plan = random.choices(plan_types[1:3], weights=[70, 30])[0]
        billing = random.choices(billing_types, weights=[55, 45])[0]
    else: # Enterprise
        plan = random.choices(plan_types[2:], weights=[60, 40])[0]
        billing = random.choices(billing_types, weights=[20, 80])[0]
        
    base_mrr = {
        "Starter": 49.0,
        "Professional": 149.0,
        "Enterprise": 499.0,
        "Custom Enterprise": 1199.0
    }[plan]
    
    discount = 0.15 if billing == "Annual" else 0.0
    effective_mrr = round(base_mrr * (1.0 - discount), 2)
    total_base_mrr += effective_mrr
    
    # ----------------------------------------------------
    # Realistic SaaS Churn Risk Dynamics
    # ----------------------------------------------------
    churn_score = 0.22
    
    # Billing cycle effect
    if billing == "Monthly":
        churn_score += 0.18
    else:
        churn_score -= 0.12
        
    # Plan effect
    if plan == "Starter":
        churn_score += 0.10
    elif plan in ["Enterprise", "Custom Enterprise"]:
        churn_score -= 0.14
        
    # Channel effect
    if "Referral" in channel:
        churn_score -= 0.08
    elif "Paid" in channel:
        churn_score += 0.06
        
    # Usage simulation
    if churn_score > 0.35:
        monthly_active_days = random.randint(1, 14)
        feature_adoption_pct = round(random.uniform(10.0, 45.0), 1)
        session_minutes_avg = round(random.uniform(4.0, 22.0), 1)
    else:
        monthly_active_days = random.randint(15, 29)
        feature_adoption_pct = round(random.uniform(50.0, 95.0), 1)
        session_minutes_avg = round(random.uniform(25.0, 110.0), 1)
        
    # Support tickets simulation
    lam = 1.8 if churn_score > 0.35 else 0.8
    # Simple poisson approximation
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    tickets_count = k - 1
    
    if tickets_count > 0:
        resolution_hours = round(random.uniform(12.0, 72.0) if churn_score > 0.35 else random.uniform(2.0, 24.0), 1)
        escalations = 1 if (churn_score > 0.35 and random.random() < 0.45) else 0
        csat = random.choice([1, 2, 3]) if churn_score > 0.35 else random.choice([4, 5, 5, 4, None])
    else:
        resolution_hours = 0.0
        escalations = 0
        csat = None
        
    if monthly_active_days < 8:
        churn_score += 0.20
    if escalations > 0:
        churn_score += 0.15
    if csat is not None and csat <= 2:
        churn_score += 0.18
        
    churn_score = max(0.02, min(0.95, churn_score))
    is_churned = random.random() < churn_score
    
    max_tenure_days = (END_DATE - signup_dt).days
    
    if is_churned and max_tenure_days > 15:
        tenure_days = min(max_tenure_days, int(exp_random(110) + 15))
        churn_dt = signup_dt + timedelta(days=tenure_days)
        if churn_dt > END_DATE:
            churn_dt = None
            is_churned = False
            status = "Active"
            churn_reason = ""
            active_count += 1
        else:
            status = "Churned"
            churn_reason = random.choice(churn_reasons)
            churned_count += 1
    else:
        churn_dt = None
        status = "Active"
        churn_reason = ""
        active_count += 1
        
    subscription_records.append({
        "subscription_id": f"SUB-{200000 + idx}",
        "customer_id": cid,
        "plan_name": plan,
        "billing_cycle": billing,
        "monthly_recurring_revenue": effective_mrr,
        "start_date": signup_dt.strftime("%Y-%m-%d"),
        "end_date": churn_dt.strftime("%Y-%m-%d") if churn_dt else "",
        "subscription_status": status,
        "churn_reason": churn_reason
    })
    
    api_calls = int(session_minutes_avg * random.randint(10, 80)) if plan in ["Enterprise", "Custom Enterprise"] else random.randint(0, 150)
    usage_records.append({
        "customer_id": cid,
        "monthly_active_days": monthly_active_days,
        "feature_adoption_rate_pct": feature_adoption_pct,
        "avg_daily_session_mins": session_minutes_avg,
        "api_calls_count": api_calls,
        "export_reports_count": random.randint(0, 45)
    })
    
    ticket_records.append({
        "customer_id": cid,
        "total_tickets_logged": tickets_count,
        "avg_resolution_time_hrs": resolution_hours,
        "escalated_tickets_count": escalations,
        "latest_csat_score": str(csat) if csat is not None else "",
        "primary_issue_category": random.choice(["Billing Inquiry", "Technical Bug", "Feature Request", "Onboarding Help"]) if tickets_count > 0 else "None"
    })

# Save Subscriptions
subs_csv = os.path.join(OUTPUT_DIR, "raw_subscriptions.csv")
with open(subs_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "subscription_id", "customer_id", "plan_name", "billing_cycle",
        "monthly_recurring_revenue", "start_date", "end_date",
        "subscription_status", "churn_reason"
    ])
    writer.writeheader()
    writer.writerows(subscription_records)
print(f"[+] Saved {len(subscription_records)} records to {subs_csv}")

# Save Usage
usage_csv = os.path.join(OUTPUT_DIR, "raw_usage_events.csv")
with open(usage_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "customer_id", "monthly_active_days", "feature_adoption_rate_pct",
        "avg_daily_session_mins", "api_calls_count", "export_reports_count"
    ])
    writer.writeheader()
    writer.writerows(usage_records)
print(f"[+] Saved {len(usage_records)} records to {usage_csv}")

# Save Tickets
tickets_csv = os.path.join(OUTPUT_DIR, "raw_support_tickets.csv")
with open(tickets_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "customer_id", "total_tickets_logged", "avg_resolution_time_hrs",
        "escalated_tickets_count", "latest_csat_score", "primary_issue_category"
    ])
    writer.writeheader()
    writer.writerows(ticket_records)
print(f"[+] Saved {len(ticket_records)} records to {tickets_csv}")

print("\n" + "="*50)
print("STAGE 1 SYNTHETIC DATA GENERATION SUCCESSFUL")
print("="*50)
print(f"Total Customer Accounts: {TOTAL_CUSTOMERS:,}")
print(f"Active Accounts        : {active_count:,} ({(active_count/TOTAL_CUSTOMERS)*100:.1f}%)")
print(f"Churned Accounts       : {churned_count:,} ({(churned_count/TOTAL_CUSTOMERS)*100:.1f}%)")
print(f"Total Base MRR Pool    : ${total_base_mrr:,.2f}")
print("="*50)
