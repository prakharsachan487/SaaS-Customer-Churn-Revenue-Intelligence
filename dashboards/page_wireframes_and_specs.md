# 3-Page Power BI Executive Dashboard Blueprint and Specifications

Technical layout specifications, chart selections, slicers, and measure assignments for the 3-page Power BI executive reporting suite.

---

## Page 1: Executive Revenue Command Center

### Primary Objective
Deliver an immediate, C-Suite overview of subscription revenue health, active subscriber counts, MRR expansion, and high-level churn impact.

### Layout Grid and Components
1. **Header and Slicers**:
   - Title: "Executive Revenue and Health Command Center"
   - Slicers: Date Range, Customer Segment (SMB, Mid-Market, Enterprise), Billing Cycle (Monthly, Annual).
2. **Top KPI Cards**:
   - `[Total Active MRR]`: Formatted as currency ($1.58M) with MoM delta indicator.
   - `[Total Active ARR]`: Formatted as currency ($19.02M).
   - `[Total Active Subscribers]`: Formatted as integer (6,532).
   - `[Customer Churn Rate %]`: Formatted as percentage (47.74%).
   - `[Avg Customer LTV]`: Formatted as currency ($1,714.00).
3. **Primary Visualizations**:
   - **Area Chart**: Monthly Recurring Revenue (MRR) Growth vs Lost Churned Revenue over 24 Months.
   - **Donut Chart**: Active MRR Contribution by Plan Tier (Starter, Professional, Enterprise, Custom).
4. **Secondary Visualizations**:
   - **Clustered Bar Chart**: Customer Acquisition Channel Performance (Active Accounts vs Churn Rate %).
   - **Horizontal Bar Chart**: Top Geographic Markets ranked by Active ARR.

---

## Page 2: Churn Drivers and Early Warning Risk Radar

### Primary Objective
Enable Customer Success leadership to identify leading indicators of account churn, evaluate machine learning feature weights, and triage critical accounts before cancellation.

### Layout Grid and Components
1. **Top KPI Cards**:
   - `[Critical High Risk Accounts]`: Count of active accounts with Health Score < 45 (1,899).
   - `[High Risk ARR at Jeopardy]`: Total ARR at immediate cancellation risk ($1.99M).
   - `[Fleet Health Score]`: Weighted telemetry index (58.4 / 100).
   - `[ML Prediction Recall]`: Model evaluation benchmark (87.50%).
2. **Primary Visualizations**:
   - **Horizontal Bar Chart**: Churn reasons ranked by lost ARR impact.
   - **Bar Chart**: Machine Learning feature importance weights (Annual Contract, Active Days, CSAT, Escalations).
3. **Actionable Table**:
   - **Customer Outreach Queue**: Filtered to active accounts with critical health scores (< 45.0) displaying Customer ID, Segment, Plan Tier, ARR, Health Score, Active Days, Support Tickets, and assigned CSM action.

---

## Page 3: Cohort Retention and Customer Lifetime Value

### Primary Objective
Provide Product Managers and Growth Marketers deep visibility into cohort decay curves, retention stabilization points, and channel LTV efficiency.

### Layout Grid and Components
1. **Interactive Simulator**:
   - What-If Parameter: Target Churn Reduction Slider (5% to 40%) calculating real-time Projected Recovered ARR ($).
2. **Primary Matrix Visual**:
   - **Cohort Retention Heatmap Matrix**:
     - Rows: Signup Cohort Month (2024-01 through 2025-12).
     - Columns: Period Number (Month 0 through Month 12).
     - Values: `[Customer Retention Rate %]`.
     - Conditional Formatting: 3-point color gradient (Green for >75%, Amber for 50-75%, Red for <50%).
3. **Secondary Visualizations**:
   - **Line Chart**: 12-Month Retention Decay Curves comparing Annual vs Monthly contract types.
   - **Bar Chart**: Average Customer Lifetime Value (LTV) by Acquisition Channel.
