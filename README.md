# ⚡ SaaS & E-Commerce Customer Churn & Revenue Intelligence Platform

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SQL Star Schema](https://img.shields.io/badge/Data%20Model-Star%20Schema-green.svg)]()
[![Power BI](https://img.shields.io/badge/Power%20BI-Executive%20Suite-F2C811.svg)]()
[![ML Model Recall](https://img.shields.io/badge/ML%20Churn%20Recall-87.5%25-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

> An end-to-end, enterprise-grade Data Analytics & Business Intelligence platform designed to analyze customer churn dynamics, predict revenue risk, calculate cohort retention, and deliver actionable C-Suite growth strategies across **12,500 customer accounts** and **$19M+ in Annual Recurring Revenue (ARR)**.

---

## 📌 Executive Summary & Business Problem

* **The Problem**: A high-growth B2B SaaS and subscription E-commerce platform observed rising customer churn (47.74% all-time churn) and significant Monthly Recurring Revenue (MRR) fluctuations. Customer Success and Product leadership lacked granular visibility into **which accounts were at immediate risk**, **why customers were leaving**, and **how cohort retention degraded month-over-month**.
* **The Solution**: Engineered an end-to-end analytics and machine learning pipeline that ingests raw subscription telemetry, transforms it into a dimensional **Star Schema**, executes advanced SQL cohort queries (`LAG`, `LEAD`, `ROW_NUMBER`), trains a predictive ML churn scoring engine (87.5% recall), and delivers a **3-Page Executive Power BI Suite** backed by 26 custom DAX measures.
* **The Financial Impact**: Identified 4 strategic C-level interventions projected to recover **+$1.18M in ARR** with a **737.5% 1-year ROI**.

---

## 🏗️ Architecture & Repository Organization

```text
├── data/
│   ├── raw/                           # 12,500+ raw records across 4 relational entities
│   │   ├── raw_customers.csv
│   │   ├── raw_subscriptions.csv
│   │   ├── raw_usage_events.csv
│   │   └── raw_support_tickets.csv
│   └── processed/                     # Cleaned dimensional Star Schema tables & SQLite database
│       ├── Dim_Customers.csv
│       ├── Dim_Plans.csv
│       ├── Dim_Date.csv
│       ├── Dim_ChurnReason.csv
│       ├── Fact_Subscriptions.csv
│       ├── Fact_Customer_Health_Score.csv
│       ├── Fact_Monthly_Cohorts.csv
│       └── saas_churn_intelligence.db # Ready-to-query relational SQLite database
├── src/
│   ├── generate_data.py               # Deterministic synthetic SaaS enterprise data generator
│   ├── etl_pipeline.py                # Automated data cleaning, type casting & Star Schema loader
│   ├── ml_churn_model.py              # ML Churn risk scoring engine (87.5% recall)
│   └── ai_insights.py                 # Automated C-Suite executive briefing generator
├── sql/
│   ├── 01_schema_ddl.sql              # Relational Star Schema DDL with PK/FK constraints
│   ├── 02_staging_and_etl.sql         # SQL cleaning, casing standardization & deduplication
│   ├── 03_cohort_analysis.sql         # Advanced CTEs & Window Functions (Month 0-12 Retention)
│   └── 04_analytical_views.sql        # High-performance KPI Views (MRR, Churn, High-Risk)
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_cohort_and_retention_deepdive.ipynb
│   └── 03_hypothesis_and_ab_testing.ipynb
├── dashboards/
│   ├── dax_measures_library.dax       # 26 Production DAX measures (MRR, ARR, NRR, LTV, Churn %)
│   ├── powerbi_data_model_guide.md    # Star Schema relationship matrix & setup guide
│   ├── page_wireframes_and_specs.md   # Visual layout specifications for Pages 1, 2, and 3
│   └── powerbi_theme.json             # Corporate Dark Fintech JSON theme for Power BI
├── docs/
│   ├── business_case_and_problem_statement.md
│   ├── executive_recommendations_and_roi.md
│   └── resume_star_bullet_points.md    # STAR bullet points tailored for resumes & interviews
├── web_preview/                       # Standalone interactive dashboard web application
│   ├── index.html
│   ├── style.css
│   └── app.js
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 3-Page Executive Power BI Dashboard Suite

| Page | Title & Target Audience | Core Visualizations & Focus Areas |
| :--- | :--- | :--- |
| **Page 1** | **Executive Overview & Revenue Command Center** *(C-Suite)* | • KPI Cards: Active MRR ($1.58M), ARR ($19.02M), Subscribers (6,532), Avg LTV ($1,714)<br>• 24-Month MRR Growth vs Lost Churn Area Chart<br>• Revenue Share by Plan Tier & Regional Market Distribution |
| **Page 2** | **Churn Drivers & Early Warning Risk Radar** *(CS & Operations)* | • Churn Reason Pareto Chart (Missing Features, High Price, Support)<br>• Customer Health Score & Usage vs Churn Scatter Matrix<br>• **High-Risk Intervention Table**: Flagged accounts with ARR in jeopardy |
| **Page 3** | **Cohort Retention & Customer Lifetime Value** *(Product & Growth)* | • **Month-over-Month Retention Heatmap Matrix (M0 to M12)**<br>• Annual vs Monthly Contract Retention Decay Curves (82% vs 38%)<br>• Acquisition Channel LTV Comparison (Referral $2,420 vs Paid $1,180)<br>• **What-If Retention & ARR Recovery Simulator** |

---

## 🧠 Advanced SQL Analytics Highlight (Cohort Retention Matrix)

```sql
-- Excerpt from sql/03_cohort_analysis.sql: Calculating Month-over-Month Cohort Retention
WITH customer_cohorts AS (
    SELECT 
        c.customer_id,
        c.cohort_month,
        s.start_date,
        s.end_date,
        s.monthly_recurring_revenue
    FROM Dim_Customers c
    JOIN Fact_Subscriptions s ON c.customer_id = s.customer_id
),
cohort_base_counts AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS total_cohort_users
    FROM customer_cohorts
    GROUP BY cohort_month
),
cohort_periods AS (
    SELECT DISTINCT year_month AS activity_month FROM Dim_Date
)
SELECT 
    cc.cohort_month,
    ((CAST(SUBSTR(cp.activity_month, 1, 4) AS INT) - CAST(SUBSTR(cc.cohort_month, 1, 4) AS INT)) * 12 +
     (CAST(SUBSTR(cp.activity_month, 6, 2) AS INT) - CAST(SUBSTR(cc.cohort_month, 6, 2) AS INT))) AS period_number,
    cb.total_cohort_users,
    COUNT(DISTINCT cc.customer_id) AS active_retained_users,
    ROUND((CAST(COUNT(DISTINCT cc.customer_id) AS REAL) / cb.total_cohort_users) * 100.0, 2) AS retention_rate_pct
FROM customer_cohorts cc
CROSS JOIN cohort_periods cp
JOIN cohort_base_counts cb ON cc.cohort_month = cb.cohort_month
WHERE cp.activity_month >= cc.cohort_month
GROUP BY cc.cohort_month, cp.activity_month
HAVING period_number BETWEEN 0 AND 12
ORDER BY cc.cohort_month, period_number;
```

---

## 💡 Top Strategic Recommendations & Financial ROI

| Strategic Initiative | Key Insight / Root Cause | Proposed Action | Projected ARR Impact | Net 1-Yr ROI |
| :--- | :--- | :--- | :--- | :--- |
| **1. Guided Onboarding Sprint** | 48% drop-off in first 60 days on Starter tier | Automated in-app checklists & milestone check-ins | **+$210,000 ARR** | **600%** |
| **2. Proactive CS Escalation SLA** | Support escalations increase churn risk by +29.3% | Auto-dispatch Senior CS Leads within 2 hrs of escalation | **+$380,000 ARR** | **633%** |
| **3. Annual Contract Migration** | Annual contracts retain at 82% vs 38% for monthly | "2 Months Free" upgrade offer on Day 60 of usage | **+$450,000 ARR** | **1,000%** |
| **4. Marketing Budget Reallocation** | Paid Ads churn at 52% while Referral churns at 28% | Shift 30% of paid ad budget to customer referral rewards | **+$140,000 ARR** | **700%** |
| **TOTAL** | | | **+$1,180,000 ARR** | **737.5% ROI** |

---

## 🚀 Quickstart Guide: How to Run

### 1. Generate Raw Data & Execute ETL Pipeline
```bash
# Generate 12,500 synthetic enterprise accounts
python src/generate_data.py

# Clean data and build Star Schema CSVs + SQLite DB
python src/etl_pipeline.py
```

### 2. Train Machine Learning Churn Engine
```bash
python src/ml_churn_model.py
```

### 3. Generate Executive Briefing
```bash
python src/ai_insights.py
```

### 4. Launch Interactive Web Dashboard Preview
Simply open `web_preview/index.html` in any modern web browser or run:
```bash
# Optional local web server
python -m http.server 8000 --directory web_preview
```
Navigate to `http://localhost:8000` to interactively explore the 3-Page Dashboard, Cohort Heatmap, and What-If Simulator!

---

## 📄 Resume & LinkedIn Presentation
For complete STAR format bullet points, check [`docs/resume_star_bullet_points.md`](docs/resume_star_bullet_points.md).
