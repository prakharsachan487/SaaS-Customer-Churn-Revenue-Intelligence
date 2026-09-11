# 3-Page Power BI Executive Dashboard Blueprint & Specifications

A detailed specification of visual layout, charts, slicers, and interactions for the 3-Page executive dashboard.

---

## 🖥️ Page 1: Executive Overview & Revenue Command Center (C-Suite View)

### Goal:
Provide executive leadership (CEO/CFO/CRO) an instantaneous snapshot of revenue health, monthly recurring revenue velocity, subscriber count, and overall churn impact.

### Layout Grid:
- **Top Header Bar**:
  - Title: *"SaaS & E-Commerce Executive Revenue & Health Command Center"*
  - Slicers: Date Range (Year/Quarter), Customer Segment (SMB / Mid-Market / Enterprise), Billing Cycle (Monthly / Annual).
- **Row 1: KPI Cards (Executive Metrics)**:
  1. `[Total Active MRR]` - Formatted as Currency ($1.58M) with MoM Delta.
  2. `[Total Active ARR]` - Formatted as Currency ($19.02M).
  3. `[Total Active Subscribers]` - Formatted as Number (6,532).
  4. `[Customer Churn Rate %]` - Formatted as Percentage (47.7%) with color alert badge.
  5. `[Avg Customer LTV]` - Formatted as Currency ($1,714).
- **Row 2: Visualizations (Center)**:
  - **Left (Area/Line Chart)**: *Monthly Recurring Revenue (MRR) Growth vs Churned Revenue Trend over 24 Months*.
    - X-Axis: `Dim_Date[year_month]`
    - Y-Axis: `[Total Active MRR]`, `[Lost Churn MRR]`
  - **Right (Donut Chart)**: *Active MRR Contribution by Plan Tier*.
    - Legend: `Dim_Plans[plan_name]` (Starter, Professional, Enterprise, Custom Enterprise)
    - Values: `[Total Active MRR]`
- **Row 3: Breakdown**:
  - **Left (Stacked Bar Chart)**: *Customer Acquisition Channel Performance (Signups vs Churn Rate %)*.
  - **Right (Matrix Table)**: *Top 5 Geographic Markets by ARR & Customer Count*.

---

## 🎯 Page 2: Churn & Risk Intelligence (Deep-Dive Analysis)

### Goal:
Empower the Chief Customer Officer (CCO) and Customer Success leads to pinpoint *why* customers are leaving, identify leading indicators (usage drop, ticket escalations), and take proactive action on high-risk accounts.

### Layout Grid:
- **Top Header Bar**:
  - Title: *"Customer Churn Drivers & Early Warning Risk Radar"*
  - Slicers: Plan Tier, Acquisition Channel, Risk Segment (High Risk / Medium Risk / Low Risk).
- **Row 1: KPI Cards**:
  1. `[Critical High Risk Accounts]` - Count of active accounts with Health Score < 45.
  2. `[High Risk ARR at Jeopardy]` - Total dollars at risk ($).
  3. `[Avg Health Score]` - Overall fleet score (0-100).
  4. `[Avg Support Resolution Time Hours]` - Operational efficiency indicator.
- **Row 2: Visualizations (Center)**:
  - **Left (Horizontal Clustered Bar Chart)**: *Churn Reasons by Lost ARR Impact*.
    - Y-Axis: `Dim_ChurnReason[churn_reason]`
    - X-Axis: `[Lost Churn ARR]`
  - **Right (Scatter Plot / Bubble Chart)**: *Customer Engagement vs Churn Likelihood*.
    - X-Axis: `Fact_Customer_Health_Score[monthly_active_days]`
    - Y-Axis: `Fact_Customer_Health_Score[feature_adoption_rate_pct]`
    - Size: `Fact_Subscriptions[monthly_recurring_revenue]`
    - Color: `Fact_Subscriptions[subscription_status]`
- **Row 3: Actionable Table (Early Warning Matrix)**:
  - Table: *High-Value At-Risk Customers (Immediate CS Outreach)*.
    - Columns: `Customer ID`, `Segment`, `Plan`, `ARR ($)`, `Health Score`, `Active Days`, `Tickets Logged`, `CSAT`.

---

## 📊 Page 3: Cohort Retention & Customer Lifetime Value (LTV)

### Goal:
Provide Product Managers and Growth Marketers deep visibility into cohort decay curves, month-over-month retention stabilization, and channel LTV efficiency.

### Layout Grid:
- **Top Header Bar**:
  - Title: *"Customer Cohort Retention & Lifetime Value (LTV) Analysis"*
  - Slicers: Signup Cohort Year, Plan Name, Billing Cycle.
- **Row 1: KPI Cards**:
  1. `[Net Revenue Retention NRR %]` - Benchmark SaaS metric (e.g. 104%).
  2. `[Average Customer Tenure]` - In Months.
  3. `[Starter Plan Month-1 Retention %]` - Onboarding drop-off benchmark.
  4. `[Annual Contract Retention Advantage %]` - Difference between Annual vs Monthly retention.
- **Row 2: The Hero Visual (Cohort Matrix Heatmap)**:
  - **Matrix Visual**:
    - Rows: `Fact_Monthly_Cohorts[cohort_month]` (e.g. 2024-01, 2024-02, ... 2025-12)
    - Columns: `Fact_Monthly_Cohorts[period_number]` (Month 0 to Month 12)
    - Values: `[Customer Retention Rate %]`
    - Conditional Formatting: Color gradient scale (Dark Green = 100% -> Yellow = 60% -> Red = 20%).
- **Row 3: Visualizations**:
  - **Left (Decay Line Chart)**: *Retention Decay Curves by Billing Cycle (Monthly vs Annual)*.
    - Demonstrates that Annual subscribers flatten out at ~82% retention while Monthly falls to ~38%.
  - **Right (Treemap / Bar Chart)**: *Average Customer Lifetime Value (LTV) by Acquisition Channel*.
    - Highlights that Referral & Organic search yield 2.4x higher LTV compared to Paid Ads.
