# Business Case & Problem Statement

## 1. Executive Context
In high-growth B2B SaaS and subscription E-commerce ecosystems, customer acquisition alone does not guarantee long-term valuation. High churn rates erode Customer Lifetime Value (LTV) and lead to unpredictable Monthly Recurring Revenue (MRR) fluctuations.

This project addresses the real-world operational challenges of a mid-to-enterprise subscription platform managing **12,500 customer accounts** and **$19M+ Annual Run Rate (ARR)**.

---

## 2. The Core Business Problem
The executive leadership team (CEO, CFO, CCO) identified critical symptoms:
1. **Retention Degradation**: Customer retention dropped below industry standard benchmarks, with an overall all-time churn rate of **47.74%**.
2. **First-90-Day Drop-Off**: High-volume early-stage churn specifically clustered in the Starter and SMB segments.
3. **Revenue Volatility**: Revenue churn disproportionately impacted accounts with frequent support escalations and low product adoption.
4. **Lack of Early Warning Visibility**: Customer Success managers lacked a unified telemetry score to intervene *before* cancellation requests occurred.

---

## 3. Project Objectives
- **Data Engineering & ETL**: Clean, deduplicate, and model raw transaction telemetry into an optimized Star Schema (`Fact_Subscriptions`, `Dim_Customers`, `Dim_Date`, `Fact_Customer_Health_Score`).
- **Advanced SQL Analytics**: Compute cohort decay matrices, Net Revenue Retention (NRR), and churn velocity using CTEs and Window Functions (`LAG`, `LEAD`).
- **Predictive ML Modeling**: Build a Churn Risk classifier (78.6% accuracy, 87.5% recall) to flag critical accounts for proactive Customer Success interventions.
- **3-Page Executive Power BI Suite**: Design an enterprise-grade dark-themed dashboard providing instant visibility into revenue health, churn drivers, and cohort retention.
- **Actionable C-Suite Playbook**: Deliver 4 quantified strategic recommendations projected to save **$1.18M+ ARR**.
