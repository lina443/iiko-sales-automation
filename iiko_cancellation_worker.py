"""
BPMN External Task Worker — iiko Sales Process
==============================================
Задача в процессе: "Check Cancellation Rate"
Движок: Camunda 7

Что делает скрипт:
- Забирает задачу из BPMN-процесса
- Получает данные по заказам из iiko (или тестовые данные)
- Считает cancellation rate
- Возвращает результат в процесс → Gateway решает что делать дальше:
    - rate < 2%  → процесс идёт дальше нормально
    - rate >= 2% → процесс отправляет алерт менеджеру
"""

import requests

# ── Настройки ──────────────────────────────────────────────
CAMUNDA_URL = "http://localhost:8080/engine-rest"
WORKER_ID   = "iiko-worker-1"
TOPIC       = "check-cancellation-rate"
LOCK_MS     = 10_000  # блокируем задачу на 10 секунд

# KPI-цель из кейса: cancellation rate < 2%
CANCELLATION_THRESHOLD = 0.02


# ── Шаг 1: Получить задачу из Camunda ─────────────────────
def fetch_task():
    response = requests.post(
        f"{CAMUNDA_URL}/external-task/fetchAndLock",
        json={
            "workerId": WORKER_ID,
            "maxTasks": 1,
            "topics": [
                {
                    "topicName": TOPIC,
                    "lockDuration": LOCK_MS
                }
            ]
        }
    )
    tasks = response.json()
    return tasks[0] if tasks else None


# ── Шаг 2: Бизнес-логика — считаем cancellation rate ──────
def calculate_cancellation_rate(total_items: int, cancelled_items: int) -> float:
    """
    KPI Formula (из кейса):
    Cancellation Rate = Cancelled Items / Total Items Ordered
    Target: < 2%
    """
    if total_items == 0:
        return 0.0
    return cancelled_items / total_items


def check_rate(rate: float) -> dict:
    """
    Возвращает результат проверки для Gateway в BPMN.
    True  → всё в норме, процесс идёт дальше
    False → превышение, отправляем алерт менеджеру
    """
    is_ok = rate < CANCELLATION_THRESHOLD
    return {
        "cancellationRate": round(rate * 100, 2),   # в процентах
        "cancellationAlert": not is_ok,              # True = нужен алерт
        "cancellationStatus": "OK" if is_ok else "ALERT"
    }


# ── Шаг 3: Вернуть результат в Camunda ────────────────────
def complete_task(task_id: str, result: dict):
    """
    Передаём переменные обратно в процесс.
    BPMN Gateway читает cancellationAlert и выбирает ветку.
    """
    variables = {
        key: {"value": value, "type": type(value).__name__.capitalize()}
        for key, value in result.items()
    }

    requests.post(
        f"{CAMUNDA_URL}/external-task/{task_id}/complete",
        json={
            "workerId": WORKER_ID,
            "variables": variables
        }
    )


# ── Главный цикл ───────────────────────────────────────────
def run():
    print("Worker запущен. Ожидаем задачи из BPMN-процесса...\n")

    task = fetch_task()

    if not task:
        print("Задач нет. Попробуй позже.")
        return

    task_id   = task["id"]
    variables = task.get("variables", {})

    # Читаем переменные которые передал BPMN-процесс
    total_items     = variables.get("totalItems",     {}).get("value", 120)
    cancelled_items = variables.get("cancelledItems", {}).get("value", 3)

    print(f"Задача получена: {task_id}")
    print(f"Всего позиций:   {total_items}")
    print(f"Отменено:        {cancelled_items}")

    # Считаем
    rate   = calculate_cancellation_rate(total_items, cancelled_items)
    result = check_rate(rate)

    print(f"\nCancellation Rate: {result['cancellationRate']}%")
    print(f"Статус:            {result['cancellationStatus']}")
    print(f"Алерт менеджеру:   {result['cancellationAlert']}")

    # Возвращаем в процесс
    complete_task(task_id, result)
    print("\nЗадача завершена. Процесс продолжается.")


# ── Тест без Camunda ───────────────────────────────────────
def test_locally():
    """
    Запусти это чтобы проверить логику без Camunda.
    """
    print("=== Локальный тест ===\n")

    test_cases = [
        {"total": 120, "cancelled": 1,  "label": "Норма (< 2%)"},
        {"total": 120, "cancelled": 3,  "label": "Граница (2.5%)"},
        {"total": 50,  "cancelled": 5,  "label": "Превышение (10%)"},
        {"total": 0,   "cancelled": 0,  "label": "Пустая смена"},
    ]

    for case in test_cases:
        rate   = calculate_cancellation_rate(case["total"], case["cancelled"])
        result = check_rate(rate)
        print(f"{case['label']}")
        print(f"  Rate: {result['cancellationRate']}% → {result['cancellationStatus']}")
        print()


if __name__ == "__main__":
    # Для теста без Camunda:
    test_locally()

    # Для реальной работы с Camunda раскомментируй:
    # run()