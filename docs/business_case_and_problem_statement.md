# Business Case and Problem Statement

## 1. Executive Context
In high-growth B2B SaaS and subscription E-commerce ecosystems, customer acquisition alone does not guarantee long-term business valuation. Unchecked churn rates erode Customer Lifetime Value (LTV) and lead to unpredictable Monthly Recurring Revenue (MRR) fluctuations.

This project addresses the operational and financial challenges of a mid-to-enterprise subscription platform managing 12,500 customer accounts and $19.02M in Annual Recurring Revenue (ARR).

---

## 2. The Core Business Problem
The executive leadership team (CEO, CFO, CCO) identified four critical operational symptoms:
1. **Retention Degradation**: Customer retention dropped below industry benchmark levels, yielding an all-time churn rate of 47.74%.
2. **First-90-Day Drop-Off**: High-volume early-stage churn concentrated in the Starter and SMB segments due to initial adoption hurdles.
3. **Revenue Volatility**: Revenue churn disproportionately impacted accounts with frequent support escalations and low product engagement.
4. **Lack of Early Warning Telemetry**: Customer Success teams lacked a unified predictive health score to intervene prior to formal cancellation requests.

---

## 3. Project Objectives
- **Data Engineering and ETL**: Clean, standardize, and model raw transaction telemetry into a production Star Schema (`Fact_Subscriptions`, `Dim_Customers`, `Dim_Date`, `Fact_Customer_Health_Score`).
- **Advanced SQL Analytics**: Compute cohort decay matrices, Net Revenue Retention (NRR), and churn velocity using CTEs and window functions (`LAG`, `LEAD`).
- **Predictive ML Modeling**: Build a Churn Risk classifier (78.60% accuracy, 87.50% recall) to identify accounts requiring proactive intervention.
- **3-Page Executive Power BI Suite**: Design a clean reporting dashboard providing visibility into revenue health, churn drivers, and cohort retention.
- **Actionable C-Suite Playbook**: Deliver 4 quantified strategic recommendations projected to save $1.18M in ARR with a 737.5% net ROI.
