-- ==============================================================================
-- 03_cohort_analysis.sql
-- Advanced SQL Analytics: Month-over-Month Cohort Retention & Churn Velocity
-- Demonstrates: CTEs, Window Functions (LAG/LEAD/ROW_NUMBER), Date Math, Aggregations
-- ==============================================================================

-- ==============================================================================
-- 1. SAAS MONTH-OVER-MONTH COHORT RETENTION MATRIX (0 TO 12 MONTHS)
-- ==============================================================================
WITH customer_cohorts AS (
    -- Step 1: Assign each customer to their original Signup Cohort Month
    SELECT 
        c.customer_id,
        c.cohort_month,
        s.start_date,
        s.end_date,
        s.monthly_recurring_revenue,
        s.subscription_status
    FROM Dim_Customers c
    JOIN Fact_Subscriptions s ON c.customer_id = s.customer_id
),
cohort_base_counts AS (
    -- Step 2: Get total starting customers and initial MRR per cohort
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS total_cohort_users,
        SUM(CAST(monthly_recurring_revenue AS REAL)) AS total_cohort_initial_mrr
    FROM customer_cohorts
    GROUP BY cohort_month
),
monthly_periods AS (
    -- Step 3: Generate 0 to 12 month interval offsets
    SELECT DISTINCT year_month AS activity_month
    FROM Dim_Date
),
cohort_retention_raw AS (
    -- Step 4: Calculate active customer count and active MRR per cohort across subsequent months
    SELECT 
        cc.cohort_month,
        mp.activity_month,
        -- Calculate period offset (Month 0, Month 1, Month 2...)
        ((CAST(SUBSTR(mp.activity_month, 1, 4) AS INT) - CAST(SUBSTR(cc.cohort_month, 1, 4) AS INT)) * 12 +
         (CAST(SUBSTR(mp.activity_month, 6, 2) AS INT) - CAST(SUBSTR(cc.cohort_month, 6, 2) AS INT))) AS period_number,
        COUNT(DISTINCT CASE 
            WHEN cc.start_date <= (mp.activity_month || '-01')
             AND (cc.end_date IS NULL OR cc.end_date = '' OR cc.end_date >= (mp.activity_month || '-01'))
            THEN cc.customer_id 
        END) AS active_retained_users,
        SUM(CASE 
            WHEN cc.start_date <= (mp.activity_month || '-01')
             AND (cc.end_date IS NULL OR cc.end_date = '' OR cc.end_date >= (mp.activity_month || '-01'))
            THEN CAST(cc.monthly_recurring_revenue AS REAL)
            ELSE 0.0
        END) AS active_retained_mrr
    FROM customer_cohorts cc
    CROSS JOIN monthly_periods mp
    WHERE mp.activity_month >= cc.cohort_month
    GROUP BY cc.cohort_month, mp.activity_month
)
SELECT 
    cr.cohort_month,
    cr.period_number,
    cb.total_cohort_users,
    cr.active_retained_users,
    -- Customer Retention Rate %
    ROUND((CAST(cr.active_retained_users AS REAL) / cb.total_cohort_users) * 100.0, 2) AS retention_rate_pct,
    -- Churn Rate %
    ROUND(100.0 - ((CAST(cr.active_retained_users AS REAL) / cb.total_cohort_users) * 100.0), 2) AS cohort_churn_pct,
    -- Net Revenue Retention %
    ROUND((cr.active_retained_mrr / cb.total_cohort_initial_mrr) * 100.0, 2) AS net_revenue_retention_nrr_pct
FROM cohort_retention_raw cr
JOIN cohort_base_counts cb ON cr.cohort_month = cb.cohort_month
WHERE cr.period_number BETWEEN 0 AND 12
ORDER BY cr.cohort_month, cr.period_number;


-- ==============================================================================
-- 2. REVENUE CHURN VELOCITY & MONTH-OVER-MONTH MRR DELTA USING LAG()
-- ==============================================================================
WITH monthly_mrr_summary AS (
    SELECT 
        d.year_month,
        SUM(CASE WHEN s.subscription_status = 'Active' THEN CAST(s.monthly_recurring_revenue AS REAL) ELSE 0 END) AS active_mrr,
        SUM(CASE WHEN s.subscription_status = 'Churned' THEN CAST(s.monthly_recurring_revenue AS REAL) ELSE 0 END) AS churned_mrr,
        COUNT(DISTINCT CASE WHEN s.subscription_status = 'Active' THEN s.customer_id END) AS active_subscribers,
        COUNT(DISTINCT CASE WHEN s.subscription_status = 'Churned' THEN s.customer_id END) AS churned_subscribers
    FROM Dim_Date d
    LEFT JOIN Fact_Subscriptions s ON SUBSTR(s.start_date, 1, 7) = d.year_month
    GROUP BY d.year_month
),
mom_lag_analysis AS (
    SELECT 
        year_month,
        active_mrr,
        churned_mrr,
        active_subscribers,
        -- LAG() Window Function to get previous month's active MRR
        LAG(active_mrr, 1) OVER (ORDER BY year_month) AS prior_month_mrr,
        -- LAG() to get prior month's active subscriber count
        LAG(active_subscribers, 1) OVER (ORDER BY year_month) AS prior_month_subscribers
    FROM monthly_mrr_summary
)
SELECT 
    year_month,
    active_mrr,
    prior_month_mrr,
    -- Net MRR Growth
    ROUND(active_mrr - COALESCE(prior_month_mrr, 0), 2) AS net_mrr_growth_dollar,
    -- MoM Growth %
    ROUND(((active_mrr - prior_month_mrr) / NULLIF(prior_month_mrr, 0)) * 100.0, 2) AS mom_mrr_growth_pct,
    -- Churn Rate %
    ROUND((churned_mrr / NULLIF(active_mrr + churned_mrr, 0)) * 100.0, 2) AS monthly_churn_rate_pct
FROM mom_lag_analysis
ORDER BY year_month;


-- ==============================================================================
-- 3. CHURN DRIVERS & AVERAGE TENURE BY SEGMENT AND BILLING CYCLE
-- ==============================================================================
SELECT 
    c.customer_segment,
    s.billing_cycle,
    s.plan_name,
    COUNT(s.subscription_id) AS total_customers,
    SUM(s.is_churned) AS total_churned,
    ROUND((CAST(SUM(s.is_churned) AS REAL) / COUNT(s.subscription_id)) * 100.0, 2) AS churn_rate_pct,
    ROUND(AVG(CAST(s.tenure_months AS REAL)), 1) AS avg_tenure_months,
    ROUND(AVG(CAST(s.customer_lifetime_value_ltv AS REAL)), 2) AS avg_ltv_usd
FROM Dim_Customers c
JOIN Fact_Subscriptions s ON c.customer_id = s.customer_id
GROUP BY c.customer_segment, s.billing_cycle, s.plan_name
ORDER BY churn_rate_pct DESC;
