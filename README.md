# ☕ iiko Sales Process Automation — BA Case Study

> **Portfolio project** · Business Analyst · Process Modeling · Python Analytics


## 📌 The Problem

A café (50 seats, 3 POS terminals) was losing revenue and staff time due to fully manual order tracking. Shift reports were compiled in Excel at the end of each day.

The daily reality:

- Revenue discrepancies between shifts — 3 to 5 per week, source unknown
- Shift closing took 40+ minutes of manual reconciliation
- Up to 8 order errors per day during peak hours
- No visibility into revenue until the shift was over


## 🎯 What Was Done

I analyzed the full sales process, identified the root causes of each problem, and designed an automation solution using the iiko POS system.

**Business outcomes:**

|Metric               |Before    |After    |Result|
|---------------------|----------|---------|------|
|Shift closing time   |40 min    |10 min   |▼ 75% |
|Revenue discrepancies|3–5 / week|0        |▼ 100%|
|Order errors         |~8 / day  |~1 / day |▼ 87% |
|Revenue visibility   |End of day|Real-time|✓ Live|


## 🗺 Process Map (BPMN)

The sales process was modeled in BPMN 2.0 across four swim lanes:

|Lane   |Responsibilities                          |
|-------|------------------------------------------|
|Guest  |Arrives, reviews menu, receives dish      |
|Waiter |Opens table in iiko, takes and sends order|
|Kitchen|Prepares dish, marks ready in iiko        |
|Cashier|Processes payment, closes check           |


## ⚙️ iiko Configuration — Key Decisions

|Feature            |Why it matters                                                    |
|-------------------|------------------------------------------------------------------|
|Table management   |Order routed to kitchen display instantly — no verbal errors      |
|Menu modifiers     |Configured dish options — reduces incorrect orders                |
|Payment integration|Card terminal linked to iiko — no manual sum entry                |
|Access control     |Discounts require manager PIN — eliminates unauthorized write-offs|
|Auto Z-report      |Shift closes automatically with full breakdown                    |
|Real-time dashboard|Revenue, avg check, cancellations visible at any moment           |


## 📋 KPI Framework

|KPI              |Formula                         |Target        |
|-----------------|--------------------------------|--------------|
|Average check    |Revenue / Number of checks      |> prev. period|
|Revenue by waiter|Sum of closed checks per waiter |Growth trend  |
|Cancellation rate|Cancelled items / Total items   |< 2%          |
|Shift close time |Time from last order to Z-report|< 15 min      |


## 🐍 Python Scripts

### `iiko_analytics.py`

Computes all KPIs from iiko export data using pandas:

- **Merge** — enriches orders with menu categories (left join to preserve all records)
- **groupby + agg** — revenue, order count, avg check per waiter
- **pivot_table** — revenue by category × shift
- **Validation** — asserts that pivot totals match raw data

### `iiko_cancellation_worker.py`

Connects Python to a BPMN process via Camunda External Task Worker:

- Fetches pending task from Camunda engine
- Calculates cancellation rate from latest data
- Returns result → BPMN gateway routes to “alert manager” or “continue”

```bash
python iiko_analytics.py
python iiko_cancellation_worker.py
```

## 📂 Repository Structure

```
.
├── iiko_analytics.py           # pandas KPI analysis
├── iiko_cancellation_worker.py # Camunda External Task Worker
├── iiko case EN.pdf            # One-page visual case study (English)
├── iiko case RU.pdf            # One-page visual case study (Russian)
└── README.md
```

## 🛠 Skills Demonstrated

- **BPMN 2.0** — full process modeling across swim lanes, AS-IS → TO-BE
- **Requirements Analysis** — stakeholder interviews, root cause identification
- **KPI Design** — metrics framework with formulas and measurable targets
- **Python / pandas** — data merging, aggregation, pivot analysis, validation
- **Camunda integration** — External Task Worker pattern, REST communication
- **Business Analysis** — translated operational pain into structured system requirements


## 👤 Author

**Karolina Gergert** — Business Analyst
Background: client relationship management, requirements documentation (BPMN, User Story Map, OpenAPI)
[linkedin.com/in/karolina-gergert-6176b2401](https://linkedin.com/in/karolina-gergert-6176b2401)