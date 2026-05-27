"""
iiko Sales Analytics — pandas
==============================
Анализ данных продаж кафе на основе кейса автоматизации iiko.

KPI из кейса:
- Average check     = Revenue / Number of checks        → цель: рост
- Revenue by waiter = Sum of closed checks per waiter   → цель: рост
- Cancellation rate = Cancelled items / Total items     → цель: < 2%
- Shift close time  = Time from last order to Z-report  → цель: < 15 min
"""

import pandas as pd
import json
from datetime import datetime

# ── 1. Тестовые данные (имитация выгрузки из iiko) ────────

orders_data = [
    {"order_id": 1,  "waiter": "Anna",  "table": 3,  "item": "Pasta",      "quantity": 2, "price": 350, "cancelled": False, "shift": "morning"},
    {"order_id": 2,  "waiter": "Anna",  "table": 3,  "item": "Coffee",     "quantity": 2, "price": 120, "cancelled": False, "shift": "morning"},
    {"order_id": 3,  "waiter": "Boris", "table": 7,  "item": "Steak",      "quantity": 1, "price": 890, "cancelled": False, "shift": "morning"},
    {"order_id": 4,  "waiter": "Boris", "table": 7,  "item": "Wine",       "quantity": 1, "price": 450, "cancelled": True,  "shift": "morning"},
    {"order_id": 5,  "waiter": "Anna",  "table": 5,  "item": "Salad",      "quantity": 3, "price": 280, "cancelled": False, "shift": "evening"},
    {"order_id": 6,  "waiter": "Anna",  "table": 5,  "item": "Juice",      "quantity": 3, "price": 150, "cancelled": False, "shift": "evening"},
    {"order_id": 7,  "waiter": "Boris", "table": 2,  "item": "Burger",     "quantity": 2, "price": 420, "cancelled": False, "shift": "evening"},
    {"order_id": 8,  "waiter": "Boris", "table": 2,  "item": "Fries",      "quantity": 2, "price": 180, "cancelled": True,  "shift": "evening"},
    {"order_id": 9,  "waiter": "Clara", "table": 9,  "item": "Soup",       "quantity": 1, "price": 220, "cancelled": False, "shift": "evening"},
    {"order_id": 10, "waiter": "Clara", "table": 9,  "item": "Tea",        "quantity": 2, "price": 90,  "cancelled": False, "shift": "evening"},
    {"order_id": 11, "waiter": "Clara", "table": 11, "item": "Cheesecake", "quantity": 2, "price": 310, "cancelled": False, "shift": "morning"},
    {"order_id": 12, "waiter": "Clara", "table": 11, "item": "Latte",      "quantity": 2, "price": 140, "cancelled": True,  "shift": "morning"},
]

menu_data = [
    {"item": "Pasta",      "category": "Main"},
    {"item": "Coffee",     "category": "Drinks"},
    {"item": "Steak",      "category": "Main"},
    {"item": "Wine",       "category": "Drinks"},
    {"item": "Salad",      "category": "Starters"},
    {"item": "Juice",      "category": "Drinks"},
    {"item": "Burger",     "category": "Main"},
    {"item": "Fries",      "category": "Starters"},
    {"item": "Soup",       "category": "Starters"},
    {"item": "Tea",        "category": "Drinks"},
    {"item": "Cheesecake", "category": "Desserts"},
    {"item": "Latte",      "category": "Drinks"},
]

# ── 2. Создаём DataFrame ───────────────────────────────────

orders = pd.DataFrame(orders_data)
menu   = pd.DataFrame(menu_data)

# Считаем выручку по каждой строке
orders["revenue"] = orders["quantity"] * orders["price"]
# Отменённые позиции не приносят выручку
orders["revenue"] = orders.apply(
    lambda row: 0 if row["cancelled"] else row["revenue"], axis=1
)

print("=" * 55)
print("  iiko Sales Analytics — KPI Report")
print("=" * 55)


# ── 3. MERGE: обогащаем заказы категориями из меню ────────
# Здесь потенциальная ловушка — используем left join
# чтобы не потерять заказы если блюда нет в справочнике

orders_enriched = pd.merge(
    orders,
    menu,
    on="item",
    how="left"   # left join — сохраняем все заказы
)

# Проверка: не потеряли ли строки после merge
assert len(orders_enriched) == len(orders), \
    f"Потеряны строки после merge! До: {len(orders)}, После: {len(orders_enriched)}"
print(f"\n✓ Merge выполнен корректно. Строк: {len(orders_enriched)}")


# ── 4. KPI 1: Cancellation Rate ────────────────────────────

total_items     = len(orders)
cancelled_items = orders["cancelled"].sum()
cancellation_rate = cancelled_items / total_items

TARGET_CANCELLATION = 0.02  # цель < 2%
status = "✓ OK" if cancellation_rate < TARGET_CANCELLATION else "✗ ALERT"

print(f"\n{'─'*55}")
print(f"  KPI 1 — Cancellation Rate")
print(f"{'─'*55}")
print(f"  Всего позиций:    {total_items}")
print(f"  Отменено:         {cancelled_items}")
print(f"  Rate:             {cancellation_rate:.1%}  (цель < 2%)")
print(f"  Статус:           {status}")


# ── 5. KPI 2: Выручка и средний чек по официантам ─────────

# groupby + agg — несколько метрик за один проход
waiter_stats = (
    orders_enriched[~orders_enriched["cancelled"]]  # только выполненные
    .groupby("waiter")
    .agg(
        total_revenue=("revenue",  "sum"),
        total_orders= ("order_id", "count"),
        avg_check=    ("revenue",  "mean")
    )
    .round(0)
    .sort_values("total_revenue", ascending=False)
)

print(f"\n{'─'*55}")
print(f"  KPI 2 — Revenue by Waiter")
print(f"{'─'*55}")
print(waiter_stats.to_string())


# ── 6. KPI 3: Выручка по категориям — pivot_table ─────────
# Строки: категория блюд, Колонки: смена, Значение: выручка
# Ловушка: aggfunc по умолчанию mean — нам нужна sum

pivot = pd.pivot_table(
    orders_enriched[~orders_enriched["cancelled"]],
    values="revenue",
    index="category",
    columns="shift",
    aggfunc="sum",    # явно указываем sum — не mean!
    fill_value=0
)

# Добавляем итоговый столбец
pivot["TOTAL"] = pivot.sum(axis=1)
pivot = pivot.sort_values("TOTAL", ascending=False)

print(f"\n{'─'*55}")
print(f"  KPI 3 — Revenue by Category & Shift")
print(f"{'─'*55}")
print(pivot.to_string())

# Контрольная проверка: итог pivot должен совпасть с общей выручкой
total_from_pivot  = pivot["TOTAL"].sum()
total_from_orders = orders_enriched["revenue"].sum()
assert total_from_pivot == total_from_orders, \
    f"Расхождение! Pivot: {total_from_pivot}, Orders: {total_from_orders}"
print(f"\n✓ Контрольная сумма совпадает: {total_from_orders:,.0f} ₽")


# ── 7. Cancellation по официантам ─────────────────────────

cancellation_by_waiter = (
    orders.groupby("waiter")
    .agg(
        total=    ("cancelled", "count"),
        cancelled=("cancelled", "sum")
    )
)
cancellation_by_waiter["rate"] = (
    cancellation_by_waiter["cancelled"] / cancellation_by_waiter["total"]
).map("{:.1%}".format)

print(f"\n{'─'*55}")
print(f"  Cancellation Rate by Waiter")
print(f"{'─'*55}")
print(cancellation_by_waiter.to_string())


# ── 8. JSON-отчёт (для передачи в BPMN / API) ─────────────

report = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "kpi": {
        "cancellation_rate":  f"{cancellation_rate:.1%}",
        "cancellation_alert": cancellation_rate >= TARGET_CANCELLATION,
        "total_revenue":      int(orders_enriched["revenue"].sum()),
        "top_waiter":         waiter_stats.index[0],
        "top_category":       pivot["TOTAL"].idxmax()
    }
}

print(f"\n{'─'*55}")
print(f"  JSON Report (для BPMN / API)")
print(f"{'─'*55}")
print(json.dumps(report, ensure_ascii=False, indent=2))
print("\n" + "=" * 55)