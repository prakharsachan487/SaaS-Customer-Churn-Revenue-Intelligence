-- ==============================================================================
-- 01_schema_ddl.sql
-- Relational Star Schema DDL for SaaS & E-Commerce Churn Intelligence
-- Compatible with PostgreSQL, MySQL 8+, SQLite, and Snowflake
-- ==============================================================================

-- 1. DIMENSION: Dim_Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    signup_date DATE NOT NULL,
    cohort_month VARCHAR(7) NOT NULL, -- Format: YYYY-MM
    acquisition_channel VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    customer_segment VARCHAR(50) NOT NULL
);

-- 2. DIMENSION: Dim_Plans
CREATE TABLE IF NOT EXISTS dim_plans (
    plan_id VARCHAR(20) PRIMARY KEY,
    plan_name VARCHAR(100) NOT NULL,
    tier_level INT NOT NULL,
    base_monthly_price DECIMAL(10, 2) NOT NULL,
    target_segment VARCHAR(50) NOT NULL
);

-- 3. DIMENSION: Dim_Date (Calendar Dimension)
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY, -- Format: YYYYMMDD
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    year_month VARCHAR(7) NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    is_weekend INT NOT NULL
);

-- 4. DIMENSION: Dim_ChurnReason
CREATE TABLE IF NOT EXISTS dim_churn_reason (
    reason_id VARCHAR(20) PRIMARY KEY,
    churn_reason VARCHAR(255) NOT NULL,
    reason_category VARCHAR(100) NOT NULL,
    impact_tier VARCHAR(50) NOT NULL
);

-- 5. FACT: Fact_Subscriptions
CREATE TABLE IF NOT EXISTS fact_subscriptions (
    subscription_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    billing_cycle VARCHAR(50) NOT NULL,
    monthly_recurring_revenue DECIMAL(10, 2) NOT NULL,
    annual_run_rate_arr DECIMAL(12, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    subscription_status VARCHAR(50) NOT NULL, -- 'Active' or 'Churned'
    is_churned INT NOT NULL,
    churn_reason VARCHAR(255),
    tenure_months INT NOT NULL,
    customer_lifetime_value_ltv DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

-- 6. FACT: Fact_Customer_Health_Score
CREATE TABLE IF NOT EXISTS fact_customer_health_score (
    customer_id VARCHAR(50) PRIMARY KEY,
    health_score DECIMAL(5, 1) NOT NULL,
    risk_segment VARCHAR(50) NOT NULL, -- 'Low Risk', 'Medium Risk', 'High Risk'
    monthly_active_days INT NOT NULL,
    feature_adoption_rate_pct DECIMAL(5, 1) NOT NULL,
    avg_daily_session_mins DECIMAL(6, 1) NOT NULL,
    api_calls_count INT NOT NULL,
    export_reports_count INT NOT NULL,
    total_tickets_logged INT NOT NULL,
    avg_resolution_time_hrs DECIMAL(6, 1) NOT NULL,
    escalated_tickets_count INT NOT NULL,
    csat_score DECIMAL(3, 1),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

-- 7. FACT: Fact_Monthly_Cohorts
CREATE TABLE IF NOT EXISTS fact_monthly_cohorts (
    cohort_month VARCHAR(7) NOT NULL,
    activity_month VARCHAR(7) NOT NULL,
    period_number INT NOT NULL,
    starting_customers INT NOT NULL,
    retained_customers INT NOT NULL,
    customer_retention_rate_pct DECIMAL(5, 2) NOT NULL,
    starting_mrr DECIMAL(12, 2) NOT NULL,
    retained_mrr DECIMAL(12, 2) NOT NULL,
    revenue_retention_rate_pct DECIMAL(5, 2) NOT NULL,
    PRIMARY KEY (cohort_month, activity_month)
);

-- CREATE INDEXES FOR FAST QUERYING & ANALYTICS
CREATE INDEX IF NOT EXISTS idx_subs_customer ON fact_subscriptions(customer_id);
CREATE INDEX IF NOT EXISTS idx_subs_status ON fact_subscriptions(subscription_status);
CREATE INDEX IF NOT EXISTS idx_subs_dates ON fact_subscriptions(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_health_risk ON fact_customer_health_score(risk_segment);
CREATE INDEX IF NOT EXISTS idx_cust_channel ON dim_customers(acquisition_channel);
