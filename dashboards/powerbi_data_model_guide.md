# Power BI Data Modeling & Relationship Guide

This document specifies the exact **Star Schema** relationships, cardinalities, cross-filter directions, and data types to establish when loading the processed CSV files into **Power BI Desktop**.

---

## 1. Relational Schema Architecture (Star Schema)

```
        +-------------------+       +-----------------------+
        |   Dim_Customers   |       |    Dim_ChurnReason    |
        +-------------------+       +-----------------------+
        | customer_id (PK)  |       | reason_id (PK)        |
        | signup_date       |       | churn_reason          |
        | acquisition_chan. |       | reason_category       |
        | country           |       | impact_tier           |
        | customer_segment  |       +-----------+-----------+
        +---------+---------+                   |
                  | 1                           | 1
                  |                             |
                  | *                           | *
        +---------v-----------------------------v-----------+
        |                Fact_Subscriptions                 |
        +---------------------------------------------------+
        | subscription_id (PK)                              |
        | customer_id (FK) -> Dim_Customers[customer_id]    |
        | plan_name (FK)    -> Dim_Plans[plan_name]         |
        | churn_reason (FK) -> Dim_ChurnReason[churn_reason]|
        | billing_cycle                                     |
        | monthly_recurring_revenue                         |
        | annual_run_rate_arr                               |
        | start_date (FK)   -> Dim_Date[full_date]          |
        | end_date (FK)     -> Dim_Date[full_date]          |
        | subscription_status                               |
        | is_churned                                        |
        | customer_lifetime_value_ltv                       |
        +---------^-----------------------------^-----------+
                  | *                           | 1
                  |                             |
                  | 1                           | 1
        +---------+---------+       +-----------+-----------+
        |     Dim_Plans     |       |       Dim_Date        |
        +-------------------+       +-----------------------+
        | plan_id (PK)      |       | date_key (PK)         |
        | plan_name         |       | full_date (Date)      |
        | tier_level        |       | year, quarter, month  |
        | base_monthly_price|       | year_month, is_weekend|
        +-------------------+       +-----------------------+
                  | 1
                  |
                  | 1 (1-to-1)
        +---------v-----------------------------+
        |      Fact_Customer_Health_Score       |
        +---------------------------------------+
        | customer_id (PK/FK)                   |
        | health_score, risk_segment            |
        | monthly_active_days                   |
        | feature_adoption_rate_pct             |
        | total_tickets_logged, csat_score      |
        +---------------------------------------+
```

---

## 2. Table-by-Table Relationship Matrix

| Primary Table (From) | Related Table (To) | From Column | To Column | Cardinality | Cross Filter Direction | Active |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Dim_Customers` | `Fact_Subscriptions` | `customer_id` | `customer_id` | 1 to Many (1:*) | Single | **Yes** |
| `Dim_Date` | `Fact_Subscriptions` | `full_date` | `start_date` | 1 to Many (1:*) | Single | **Yes** (Primary) |
| `Dim_Date` | `Fact_Subscriptions` | `full_date` | `end_date` | 1 to Many (1:*) | Single | **No** (Use via `USERELATIONSHIP`) |
| `Dim_Plans` | `Fact_Subscriptions` | `plan_name` | `plan_name` | 1 to Many (1:*) | Single | **Yes** |
| `Dim_ChurnReason`| `Fact_Subscriptions`| `churn_reason`| `churn_reason`| 1 to Many (1:*) | Single | **Yes** |
| `Dim_Customers` | `Fact_Customer_Health_Score` | `customer_id` | `customer_id` | 1 to 1 (1:1) | Both | **Yes** |

---

## 3. Power BI Setup Instructions
1. **Import Data**: In Power BI Desktop, click **Get Data** -> **Folder** or **Text/CSV** -> Select the `data/processed/` folder.
2. **Mark as Date Table**: Right-click `Dim_Date` in Model View -> **Mark as date table** -> Select `full_date`.
3. **Hide Foreign Key Columns**: Hide raw ID columns in Fact tables (`customer_id`, `plan_name`) to ensure report builders filter via Dimension tables.
4. **Create Measure Table**: Create a blank table called `_Measures` and paste the DAX measures from `dashboards/dax_measures_library.dax`.
