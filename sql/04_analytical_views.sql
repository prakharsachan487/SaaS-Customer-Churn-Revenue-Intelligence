-- ==============================================================================
-- 04_analytical_views.sql
-- High-Performance Executive Analytical Views
-- Optimized for BI Dashboards and Automated Executive Reporting
-- ==============================================================================

-- 1. EXECUTIVE KPI SUMMARY VIEW
CREATE VIEW IF NOT EXISTS vw_executive_kpis AS
SELECT 
    COUNT(DISTINCT s.customer_id) AS total_customers_all_time,
    COUNT(DISTINCT CASE WHEN s.subscription_status = 'Active' THEN s.customer_id END) AS active_subscribers,
    COUNT(DISTINCT CASE WHEN s.subscription_status = 'Churned' THEN s.customer_id END) AS churned_customers,
    ROUND((CAST(COUNT(DISTINCT CASE WHEN s.subscription_status = 'Churned' THEN s.customer_id END) AS REAL) / COUNT(DISTINCT s.customer_id)) * 100.0, 2) AS overall_churn_rate_pct,
    ROUND(SUM(CASE WHEN s.subscription_status = 'Active' THEN CAST(s.monthly_recurring_revenue AS REAL) ELSE 0 END), 2) AS current_mrr,
    ROUND(SUM(CASE WHEN s.subscription_status = 'Active' THEN CAST(s.annual_run_rate_arr AS REAL) ELSE 0 END), 2) AS current_arr,
    ROUND(AVG(CAST(s.customer_lifetime_value_ltv AS REAL)), 2) AS avg_customer_ltv,
    ROUND(AVG(CAST(s.tenure_months AS REAL)), 1) AS avg_customer_tenure_months
FROM Fact_Subscriptions s;

-- 2. CHURN REASONS & REVENUE AT RISK BREAKDOWN
CREATE VIEW IF NOT EXISTS vw_churn_reasons_breakdown AS
SELECT 
    COALESCE(s.churn_reason, 'Active / Not Churned') AS churn_reason,
    COUNT(s.subscription_id) AS customer_count,
    ROUND(SUM(CAST(s.monthly_recurring_revenue AS REAL)), 2) AS total_mrr_impact,
    ROUND(SUM(CAST(s.annual_run_rate_arr AS REAL)), 2) AS total_arr_impact,
    ROUND(AVG(CAST(s.tenure_months AS REAL)), 1) AS avg_tenure_before_churn
FROM Fact_Subscriptions s
WHERE s.subscription_status = 'Churned'
GROUP BY s.churn_reason
ORDER BY total_arr_impact DESC;

-- 3. HIGH-RISK EARLY WARNING ACCOUNTS (TOP INTERVENTION LIST)
CREATE VIEW IF NOT EXISTS vw_high_risk_early_warning AS
SELECT 
    c.customer_id,
    c.customer_segment,
    s.plan_name,
    s.billing_cycle,
    CAST(s.monthly_recurring_revenue AS REAL) AS mrr,
    CAST(s.annual_run_rate_arr AS REAL) AS arr,
    h.health_score,
    h.risk_segment,
    h.monthly_active_days,
    h.feature_adoption_rate_pct,
    h.total_tickets_logged,
    h.escalated_tickets_count,
    h.csat_score
FROM Dim_Customers c
JOIN Fact_Subscriptions s ON c.customer_id = s.customer_id
JOIN Fact_Customer_Health_Score h ON c.customer_id = h.customer_id
WHERE s.subscription_status = 'Active' 
  AND h.risk_segment = 'High Risk (Critical)'
ORDER BY arr DESC;

-- 4. ACQUISITION CHANNEL PERFORMANCE & LTV:CAC VIEW
CREATE VIEW IF NOT EXISTS vw_channel_performance AS
SELECT 
    c.acquisition_channel,
    COUNT(c.customer_id) AS total_signups,
    SUM(s.is_churned) AS churned_count,
    ROUND((CAST(SUM(s.is_churned) AS REAL) / COUNT(c.customer_id)) * 100.0, 2) AS channel_churn_rate_pct,
    ROUND(SUM(CAST(s.monthly_recurring_revenue AS REAL)), 2) AS total_mrr_generated,
    ROUND(AVG(CAST(s.customer_lifetime_value_ltv AS REAL)), 2) AS avg_ltv_usd
FROM Dim_Customers c
JOIN Fact_Subscriptions s ON c.customer_id = s.customer_id
GROUP BY c.acquisition_channel
ORDER BY total_mrr_generated DESC;
