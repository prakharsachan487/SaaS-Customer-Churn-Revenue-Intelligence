# SaaS and E-Commerce Customer Churn and Revenue Intelligence Platform

A comprehensive Data Analytics and Business Intelligence engineering repository analyzing subscription churn dynamics, calculating customer lifetime value (LTV), predicting cancellation risk, and modeling revenue retention across 12,500 customer accounts and $19.02M in Annual Recurring Revenue (ARR).

---

## 1. Problem Statement and Objectives

High-growth SaaS and subscription commerce businesses face revenue volatility when customer churn outpaces expansion. This project addresses the operational and financial challenges of subscription churn by delivering:

- **End-to-End ETL Pipeline**: Ingesting and transforming raw multi-table customer telemetry into an optimized Star Schema and analytical SQLite data warehouse.
- **Advanced SQL Analytics**: Computing month-over-month cohort retention matrices (Month 0 to Month 12) and revenue velocity using CTEs and window functions (`LAG`, `LEAD`, `ROW_NUMBER`).
- **Machine Learning Risk Scoring**: Training a logistic regression classification model (87.5% recall) to flag accounts at risk before cancellation.
- **Executive Power BI Dashboard**: Architecting a 3-page reporting suite backed by 26 production DAX measures (MRR, ARR, NRR, LTV, ARPU).
- **Financial Impact Modeling**: Formulating 4 strategic interventions projected to recover $1.18M ARR with an estimated 737.5% first-year ROI.

---

## 2. Repository Architecture

```text
├── data/
│   ├── raw/                           # Raw transaction tables (12,500 records)
│   │   ├── raw_customers.csv
│   │   ├── raw_subscriptions.csv
│   │   ├── raw_usage_events.csv
│   │   └── raw_support_tickets.csv
│   └── processed/                     # Cleaned dimensional Star Schema tables
│       ├── Dim_Customers.csv
│       ├── Dim_Plans.csv
│       ├── Dim_Date.csv
│       ├── Dim_ChurnReason.csv
│       ├── Fact_Subscriptions.csv
│       ├── Fact_Customer_Health_Score.csv
│       ├── Fact_Monthly_Cohorts.csv
│       └── saas_churn_intelligence.db # Relational SQLite warehouse
├── src/
│   ├── generate_data.py               # Deterministic synthetic data generator
│   ├── etl_pipeline.py                # Data cleaning, type casting, and Star Schema loader
│   ├── ml_churn_model.py              # ML risk scoring engine and feature importance
│   └── ai_insights.py                 # Automated C-Suite executive briefing generator
├── sql/
│   ├── 01_schema_ddl.sql              # Relational DDL with PK/FK constraints and indexes
│   ├── 02_staging_and_etl.sql         # SQL cleaning, casing standardization, deduplication
│   ├── 03_cohort_analysis.sql         # Advanced CTEs and Window Functions (M0-M12 Retention)
│   └── 04_analytical_views.sql        # Production KPI and early warning views
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_cohort_and_retention_deepdive.ipynb
│   └── 03_hypothesis_and_ab_testing.ipynb
├── dashboards/
│   ├── SaaS_Churn_Revenue_Intelligence.pbix # Complete 3-page Power BI Dashboard file
│   ├── dax_measures_library.dax       # 26 production DAX measures
│   ├── powerbi_data_model_guide.md    # Star Schema relationship matrix and model setup
│   ├── page_wireframes_and_specs.md   # UI/UX specifications for Pages 1, 2, and 3
│   └── powerbi_theme.json             # Corporate executive theme for Power BI Desktop
├── docs/
│   ├── business_case_and_problem_statement.md
│   ├── executive_recommendations_and_roi.md
│   └── resume_star_bullet_points.md    # STAR bullet points for resumes and interviews
├── web_preview/                       # Interactive browser dashboard preview
│   ├── index.html
│   ├── style.css
│   └── app.js
├── package.json
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 3. Core Metrics and Baseline Performance

| Metric | Value | Description |
| :--- | :--- | :--- |
| **Total Monitored Accounts** | 12,500 | Total customer volume across SMB, Mid-Market, and Enterprise |
| **Active Subscribers** | 6,532 | Current active paying customer base (52.3% active rate) |
| **Active MRR** | $1,584,703 | Total current Monthly Recurring Revenue |
| **Active ARR** | $19,016,437 | Annualized revenue run rate (MRR x 12) |
| **All-Time Churn Rate** | 47.74% | 5,968 historical cancellations |
| **Average Customer LTV** | $1,714.00 | Blended lifetime value across all plans and tenures |
| **Average Customer Tenure** | 8.0 Months | Average retention lifespan before cancellation |

---

## 4. Advanced SQL Analytics

The following query from `sql/03_cohort_analysis.sql` demonstrates the calculation of month-over-month cohort retention rates from Month 0 to Month 12 using Common Table Expressions (CTEs) and date math:

```sql
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

## 5. Machine Learning Churn Scoring Model

A classification pipeline was developed in `src/ml_churn_model.py` to evaluate churn hazard across multiple engagement and support indicators:

- **Accuracy**: 78.60%
- **Recall**: 87.50% (prioritized to minimize missed at-risk accounts)
- **Precision**: 72.62%
- **F1-Score**: 79.37%

### Feature Importance Weights:
1. **Annual Contract**: -0.4724 (Substantially reduces churn risk)
2. **Monthly Active Days**: -0.3645 (Higher usage reduces churn)
3. **CSAT Score**: -0.3340 (Higher satisfaction protects retention)
4. **Escalated Tickets**: +0.2928 (Strongest operational churn driver)
5. **Starter Plan**: +0.1932 (Higher onboarding drop-off risk)

---

## 6. Power BI Dashboard Specifications

The business intelligence suite is structured into three dedicated report pages:

1. **Page 1: Executive Revenue Command Center**
   - KPI Cards: Total Active MRR, ARR, Active Subscribers, Churn Rate %, Average LTV.
   - Area Chart: 24-Month Active MRR Growth vs Lost Churned Revenue.
   - Donut Chart: Revenue contribution by Plan Tier (Starter, Professional, Enterprise, Custom).
   - Horizontal Bar: Revenue by Geographic Markets.

2. **Page 2: Churn Drivers and Risk Radar**
   - Horizontal Clustered Bar: Churn reasons ranked by lost ARR impact.
   - Feature Importance Bar: Machine learning coefficients ranking churn drivers.
   - Early Warning Action Table: Active accounts with health score < 45 for proactive Customer Success outreach.

3. **Page 3: Cohort Retention and Lifetime Value**
   - Heatmap Matrix: Month-over-Month retention decay (Month 0 to Month 12).
   - Line Chart: Retention decay curves comparing Annual vs Monthly billing cycles.
   - Bar Chart: Average Customer Lifetime Value (LTV) by Acquisition Channel.
   - Interactive What-If Parameter: ARR recovery simulator based on targeted churn reduction.

---

## 7. Strategic Recommendations and Financial ROI

| Strategic Initiative | Root Cause Identified | Recommended Action | Projected ARR Impact | Net 1-Year ROI |
| :--- | :--- | :--- | :--- | :--- |
| **1. Guided Onboarding Sprint** | 48% drop-off in first 60 days on Starter tier | In-app milestone checklists and guided setup | **+$210,000 ARR** | **600%** |
| **2. CS Escalation SLA** | Escalations increase churn probability by 29.3% | Auto-dispatch Senior CS Leads within 2 hours | **+$380,000 ARR** | **633%** |
| **3. Annual Contract Migration** | Monthly accounts churn 2.8x faster than annual | "2 Months Free" upgrade incentive at Day 60 | **+$450,000 ARR** | **1,000%** |
| **4. Marketing Budget Reallocation** | Paid Ads churn at 52% vs Referral at 28% | Shift 30% of paid ad budget to referral incentives | **+$140,000 ARR** | **700%** |
| **TOTAL** | | | **+$1,180,000 ARR** | **737.5% ROI** |

---

## 8. Execution Instructions

### Prerequisites
- Python 3.9+
- Node.js (Optional, for npm dev server)

### Step 1: Generate Data and Run ETL
```bash
python src/generate_data.py
python src/etl_pipeline.py
```

### Step 2: Train Machine Learning Model
```bash
python src/ml_churn_model.py
```

### Step 3: Run AI Executive Briefing
```bash
python src/ai_insights.py
```

### Step 4: Launch Web Dashboard
```bash
npm run dev
# Or open web_preview/index.html in any browser
```
Access the application locally at `http://localhost:3000`.

---

## 9. License
Distributed under the MIT License. See `LICENSE` for more information.
