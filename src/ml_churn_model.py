"""
ml_churn_model.py
-----------------
Predictive Machine Learning Engine for SaaS Customer Churn & Risk Scoring.

Builds a predictive classification pipeline to score customer churn likelihood,
extract feature importance weights, and generate proactive risk classifications.
Includes zero-dependency mathematical fallback so it executes in any environment.
"""

import os
import csv
import math
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def read_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

print("[*] Loading processed datasets for ML Churn Model training...")

customers = {r["customer_id"]: r for r in read_csv(os.path.join(PROCESSED_DIR, "Dim_Customers.csv"))}
subs = {r["customer_id"]: r for r in read_csv(os.path.join(PROCESSED_DIR, "Fact_Subscriptions.csv"))}
health = {r["customer_id"]: r for r in read_csv(os.path.join(PROCESSED_DIR, "Fact_Customer_Health_Score.csv"))}

# Prepare Feature Matrix
# Features:
# 1. is_annual_contract (0 or 1)
# 2. is_starter_plan (0 or 1)
# 3. is_enterprise_plan (0 or 1)
# 4. monthly_active_days (1-30)
# 5. feature_adoption_rate_pct (0-100)
# 6. avg_daily_session_mins (0-200)
# 7. total_tickets_logged (0-10)
# 8. escalated_tickets_count (0 or 1)
# 9. csat_score (1.0-5.0)

dataset = []
for cid, sub in subs.items():
    h = health.get(cid, {})
    c = customers.get(cid, {})
    
    is_annual = 1.0 if sub["billing_cycle"] == "Annual" else 0.0
    is_starter = 1.0 if sub["plan_name"] == "Starter" else 0.0
    is_enterprise = 1.0 if "Enterprise" in sub["plan_name"] else 0.0
    
    act_days = float(h.get("monthly_active_days", 15))
    adopt_pct = float(h.get("feature_adoption_rate_pct", 50))
    session_mins = float(h.get("avg_daily_session_mins", 30))
    tickets = float(h.get("total_tickets_logged", 0))
    escalated = float(h.get("escalated_tickets_count", 0))
    csat = float(h.get("csat_score", 3.5)) if h.get("csat_score") else 3.5
    
    target_churn = float(sub["is_churned"])
    
    dataset.append({
        "customer_id": cid,
        "features": [
            is_annual, is_starter, is_enterprise, act_days,
            adopt_pct, session_mins, tickets, escalated, csat
        ],
        "target": target_churn,
        "mrr": float(sub["monthly_recurring_revenue"]),
        "status": sub["subscription_status"]
    })

# Train-Test Split (80 / 20)
random.seed(42)
random.shuffle(dataset)
split_idx = int(len(dataset) * 0.8)
train_data = dataset[:split_idx]
test_data = dataset[split_idx:]

feature_names = [
    "Annual Contract", "Starter Plan", "Enterprise Plan", "Monthly Active Days",
    "Feature Adoption %", "Avg Daily Session Mins", "Total Tickets Logged",
    "Escalated Tickets", "CSAT Score"
]

print(f"[+] Total Records: {len(dataset):,} (Train: {len(train_data):,}, Test: {len(test_data):,})")

# Feature Scaling (Standardization)
num_features = len(feature_names)
means = [0.0] * num_features
stds = [0.0] * num_features

for row in train_data:
    for j in range(num_features):
        means[j] += row["features"][j]

means = [m / len(train_data) for m in means]

for row in train_data:
    for j in range(num_features):
        stds[j] += (row["features"][j] - means[j]) ** 2

stds = [math.sqrt(s / len(train_data)) or 1.0 for s in stds]

def scale_features(feats):
    return [(feats[j] - means[j]) / stds[j] for j in range(num_features)]

# Logistic Regression Classifier (Gradient Descent)
weights = [0.0] * num_features
bias = 0.0
lr = 0.08
epochs = 200

print("[*] Training Logistic Churn Risk Scoring Engine...")

for epoch in range(epochs):
    grad_w = [0.0] * num_features
    grad_b = 0.0
    
    for row in train_data:
        x_norm = scale_features(row["features"])
        y = row["target"]
        
        # Logit
        z = bias + sum(w * x for w, x in zip(weights, x_norm))
        z = max(-20.0, min(20.0, z)) # Prevent overflow
        p = 1.0 / (1.0 + math.exp(-z))
        
        err = p - y
        for j in range(num_features):
            grad_w[j] += err * x_norm[j]
        grad_b += err
        
    n = len(train_data)
    for j in range(num_features):
        weights[j] -= lr * (grad_w[j] / n)
    bias -= lr * (grad_b / n)

# Evaluate on Test Set
true_pos = 0
true_neg = 0
false_pos = 0
false_neg = 0

for row in test_data:
    x_norm = scale_features(row["features"])
    z = bias + sum(w * x for w, x in zip(weights, x_norm))
    z = max(-20.0, min(20.0, z))
    prob = 1.0 / (1.0 + math.exp(-z))
    pred = 1.0 if prob >= 0.5 else 0.0
    y = row["target"]
    
    if pred == 1.0 and y == 1.0:
        true_pos += 1
    elif pred == 0.0 and y == 0.0:
        true_neg += 1
    elif pred == 1.0 and y == 0.0:
        false_pos += 1
    else:
        false_neg += 1

accuracy = (true_pos + true_neg) / len(test_data) * 100
precision = (true_pos / (true_pos + false_pos)) * 100 if (true_pos + false_pos) > 0 else 0.0
recall = (true_pos / (true_pos + false_neg)) * 100 if (true_pos + false_neg) > 0 else 0.0
f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

print("\n" + "="*50)
print("MACHINE LEARNING CHURN MODEL EVALUATION")
print("="*50)
print(f"Accuracy : {accuracy:.2f}%")
print(f"Precision: {precision:.2f}%")
print(f"Recall   : {recall:.2f}%")
print(f"F1-Score : {f1:.2f}%")
print("="*50)

# Feature Importance
print("\n[TOP CHURN DRIVERS & FEATURE WEIGHTS]:")
feature_importance = sorted(zip(feature_names, weights), key=lambda x: abs(x[1]), reverse=True)
for feat, w in feature_importance:
    direction = "INCREASES CHURN RISK (+)" if w > 0 else "REDUCES CHURN RISK (-)"
    print(f"  * {feat:<24}: Weight = {w:+.4f} | {direction}")

# Generate Predictions Export for Active Accounts
predictions_export = []
for row in dataset:
    if row["status"] == "Active":
        x_norm = scale_features(row["features"])
        z = bias + sum(w * x for w, x in zip(weights, x_norm))
        z = max(-20.0, min(20.0, z))
        prob = round(1.0 / (1.0 + math.exp(-z)), 4)
        
        risk_label = "High Risk" if prob >= 0.65 else ("Medium Risk" if prob >= 0.35 else "Low Risk")
        
        predictions_export.append({
            "customer_id": row["customer_id"],
            "current_mrr": row["mrr"],
            "annual_arr": round(row["mrr"] * 12, 2),
            "churn_probability": prob,
            "predicted_risk_tier": risk_label
        })

pred_csv = os.path.join(PROCESSED_DIR, "Fact_ML_Churn_Predictions.csv")
with open(pred_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id", "current_mrr", "annual_arr", "churn_probability", "predicted_risk_tier"])
    writer.writeheader()
    writer.writerows(predictions_export)

print(f"\n[+] Generated proactive ML Churn Predictions for {len(predictions_export):,} active accounts at {pred_csv}")
