☕ iiko Sales Process Automation — BA Case Study

Portfolio project · Business Analyst · Process Modeling · Python Analytics

A real business analysis case: automating the full sales cycle in a café using the iiko POS system — from table opening to shift close.

📌 Context
A café (50 seats, 3 POS terminals) faced recurring operational issues:

Revenue discrepancies between shifts
Slow shift closing (40+ minutes)
Order errors during peak hours
No real-time visibility into revenue

All order tracking was manual. Shift reports were compiled in Excel.

🎯 Goal
Automate the full sales cycle using iiko POS — reducing human error and providing real-time visibility into revenue and staff performance.

📂 Repository Structure
.
├── docs/
│   └── iiko_sales_case.pdf          # One-page visual case study
├── iiko_analytics.py                # pandas KPI analysis script
├── iiko_cancellation_worker.py      # Python BPMN External Task Worker (Camunda)
└── README.md

🗺 Process Map (BPMN)
The sales process was modeled in BPMN 2.0 across four swim lanes:
LaneResponsibilitiesGuestArrives, reviews menu, receives dishWaiterOpens table in iiko, takes and sends orderKitchenPrepares dish, marks ready in iikoCashierProcesses payment, closes check

⚙️ Solution — iiko Configuration
FeatureBusiness ImpactTable managementOrder routed to kitchen display instantly — no verbal errorsMenu modifiersConfigured dish options — reduces incorrect ordersPayment integrationCard terminal linked to iiko — no manual sum entryAccess controlDiscounts require manager PIN — eliminates unauthorized write-offsAuto Z-reportShift closes automatically with full breakdownReal-time dashboardRevenue, avg check, cancellations visible at any moment

📊 Results
MetricBeforeAfterResultShift closing time40 min10 min▼ 75%Revenue discrepancies3–5 / week0▼ 100%Order errors~8 / day~1 / day▼ 87%Revenue visibilityEnd of dayReal-time✓ Live

📋 KPI Framework
KPIFormulaTargetAverage checkRevenue / Number of checks> prev. periodRevenue by waiterSum of closed checks per waiterGrowth trendCancellation rateCancelled items / Total items< 2%Shift close timeTime from last order to Z-report< 15 min

🐍 Python Analytics
iiko_analytics.py
pandas script that computes all KPIs from iiko export data:

Merge — enriches orders with menu categories (left join to avoid data loss)
groupby + agg — revenue, order count, avg check per waiter
pivot_table — revenue by category × shift (explicit aggfunc="sum")
Validation — asserts that pivot totals match raw data (control sum)
JSON report — outputs KPI summary ready for BPMN / API consumption

bashpython iiko_analytics.py
iiko_cancellation_worker.py
Camunda External Task Worker — connects Python to a BPMN process:

Fetches task from Camunda engine
Calculates cancellation rate
Returns result to process → Gateway routes to "alert manager" or "continue"

bashpython iiko_cancellation_worker.py  # runs local test by default

📝 User Story

As a waiter,
I want to open a table in iiko and take an order,
so that the kitchen receives it instantly without verbal communication,
and the check is automatically formed for the guest.


🛠 Skills Demonstrated

BPMN 2.0 — full process modeling across swim lanes
Requirements Analysis — AS-IS → TO-BE, stakeholder interviews
KPI Design — metrics framework with formulas and targets
Python / pandas — merge, groupby, pivot_table, data validation
Camunda integration — External Task Worker pattern
REST / JSON — API communication between Python and BPMN engine


👤 Author
Karolina Gergert — Business Analyst
📍 Buenos Aires, Argentina
linkedin.com/in/karolina-gergert-6176b2401

This project is part of a BA portfolio demonstrating real-world process analysis and automation skills.