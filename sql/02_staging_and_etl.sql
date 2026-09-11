-- ==============================================================================
-- 02_staging_and_etl.sql
-- Staging Data Ingestion, Cleaning & Dimension Transformation
-- ==============================================================================

-- 1. STAGING TABLE CLEANING EXAMPLE
-- Standardizing acquisition channels, trimming whitespace and resolving casing issues
WITH cleaned_raw_customers AS (
    SELECT 
        TRIM(customer_id) AS customer_id,
        CAST(signup_date AS DATE) AS signup_date,
        CASE 
            WHEN LOWER(TRIM(acquisition_channel)) = 'outbound_sales' THEN 'Outbound Sales'
            WHEN LOWER(TRIM(acquisition_channel)) = 'paid ads' THEN 'Paid Ads'
            WHEN LOWER(TRIM(acquisition_channel)) = 'organic search' THEN 'Organic Search'
            WHEN LOWER(TRIM(acquisition_channel)) = 'email campaign' THEN 'Email Campaign'
            WHEN LOWER(TRIM(acquisition_channel)) = 'social media' THEN 'Social Media'
            WHEN LOWER(TRIM(acquisition_channel)) = 'direct' THEN 'Direct'
            WHEN LOWER(TRIM(acquisition_channel)) = 'referral' THEN 'Referral'
            ELSE INITCAP(TRIM(acquisition_channel))
        END AS acquisition_channel,
        TRIM(country) AS country,
        TRIM(customer_segment) AS customer_segment,
        SUBSTR(signup_date, 1, 7) AS cohort_month
    FROM raw_customers
    WHERE customer_id IS NOT NULL
)
SELECT * FROM cleaned_raw_customers;

-- 2. DEDUPLICATION & NULL HANDLING LOGIC
-- Ensuring each customer has a single unique primary subscription record
WITH ranked_subscriptions AS (
    SELECT 
        subscription_id,
        customer_id,
        plan_name,
        billing_cycle,
        CAST(monthly_recurring_revenue AS DECIMAL(10,2)) AS mrr,
        CAST(start_date AS DATE) AS start_date,
        CAST(NULLIF(end_date, '') AS DATE) AS end_date,
        COALESCE(subscription_status, 'Active') AS subscription_status,
        NULLIF(TRIM(churn_reason), '') AS churn_reason,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY start_date DESC
        ) AS rn
    FROM raw_subscriptions
)
SELECT * FROM ranked_subscriptions WHERE rn = 1;
