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

## RU
# ☕ Автоматизация продаж в кафе — кейс бизнес-аналитика

> **Портфолио-проект** · Бизнес-аналитик · Моделирование процессов · Python-аналитика

-----

## 📌 Проблема

Кафе на 50 мест с 3 кассовыми терминалами теряло выручку и рабочее время из-за полностью ручного учёта заказов. Отчёты по сменам формировались вручную в Excel в конце дня.

Ежедневная картина:

- Расхождения в кассе — 3–5 в неделю, причина неизвестна
- Закрытие смены занимало 40+ минут ручной сверки
- До 8 ошибок в заказах в день в час пик
- Видимость выручки — только после закрытия смены

-----

## 🎯 Что было сделано

Я проанализировала весь процесс продаж, выявила первопричины каждой проблемы и разработала решение по автоматизации через POS-систему iiko.

**Бизнес-результаты:**

|Метрика               |До       |После         |Результат|
|----------------------|---------|--------------|---------|
|Время закрытия смены  |40 мин   |10 мин        |▼ 75%    |
|Расхождения по выручке|3–5 / нед|0             |▼ 100%   |
|Ошибки в заказах      |~8 / день|~1 / день     |▼ 87%    |
|Видимость выручки     |Конец дня|Реальное время|✓ Live   |

-----

## 🗺 Карта процесса (BPMN)

Процесс продаж смоделирован в нотации BPMN 2.0 в четырёх дорожках:

|Дорожка |Зона ответственности                               |
|--------|---------------------------------------------------|
|Гость   |Приходит, выбирает блюдо, получает заказ           |
|Официант|Открывает стол в iiko, принимает и отправляет заказ|
|Кухня   |Готовит блюдо, отмечает готовность в iiko          |
|Кассир  |Проводит оплату, закрывает чек                     |

-----

## ⚙️ Настройка iiko — ключевые решения

|Функция                   |Почему это важно                                                     |
|--------------------------|---------------------------------------------------------------------|
|Управление столами        |Заказ моментально уходит на кухонный экран — без устной передачи     |
|Модификаторы меню         |Настроены опции блюд — снижают число неверных заказов                |
|Интеграция с эквайрингом  |Терминал оплаты связан с iiko — нет ручного ввода суммы              |
|Контроль прав доступа     |Скидки требуют PIN менеджера — исключают несанкционированные списания|
|Авто Z-отчёт              |Смена закрывается автоматически с полной разбивкой                   |
|Дашборд в реальном времени|Выручка, средний чек, отмены — видны в любой момент                  |

-----

## 📋 KPI-фреймворк

|KPI                 |Формула                               |Целевое значение     |
|--------------------|--------------------------------------|---------------------|
|Средний чек         |Выручка / Количество чеков            |> предыдущего периода|
|Выручка по официанту|Сумма закрытых чеков по сотруднику    |Динамика роста       |
|Процент отмен       |Отменённые позиции / Всего позиций    |< 2%                 |
|Время закрытия смены|Время от последнего заказа до Z-отчёта|< 15 мин             |

-----

## 🐍 Python-скрипты

### `iiko_analytics.py`

Вычисляет все KPI по выгрузке из iiko с помощью pandas:

- **merge** — обогащение заказов категориями меню (left join, чтобы не потерять данные)
- **groupby + agg** — выручка, количество заказов, средний чек по официантам
- **pivot_table** — выручка по категориям × смена
- **Валидация** — проверка, что итоги сводной совпадают с исходными данными

### `iiko_cancellation_worker.py`

Подключает Python к BPMN-процессу через External Task Worker Camunda:

- Забирает задачу из движка Camunda
- Вычисляет процент отмен по актуальным данным
- Возвращает результат → шлюз BPMN направляет к «уведомить менеджера» или «продолжить»

```bash
python iiko_analytics.py
python iiko_cancellation_worker.py
```

-----

## 📂 Структура репозитория

```
.
├── iiko_analytics.py           # pandas-анализ KPI
├── iiko_cancellation_worker.py # Camunda External Task Worker
├── iiko case EN.pdf            # Визуальный кейс (английский)
├── iiko case RU.pdf            # Визуальный кейс (русский)
└── README.md
```

-----

## 🛠 Продемонстрированные навыки

- **BPMN 2.0** — полное моделирование процесса с дорожками, AS-IS → TO-BE
- **Анализ требований** — интервью со стейкхолдерами, поиск первопричин
- **Проектирование KPI** — метрики с формулами и измеримыми целями
- **Python / pandas** — объединение данных, агрегация, сводный анализ, контроль качества
- **Интеграция с Camunda** — паттерн External Task Worker, REST-взаимодействие
- **Бизнес-анализ** — перевод операционных болей в структурированные системные требования

-----

## 👤 Автор

**Каролина Гергерт** — Бизнес-аналитик
Опыт: управление клиентскими отношениями, документирование требований (BPMN, User Story Map, OpenAPI)
[linkedin.com/in/karolina-gergert-6176b2401](https://linkedin.com/in/karolina-gergert-6176b2401)