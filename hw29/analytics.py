from typing import Any

orders_count = 0
payments_count  = 0

def log_order_created(data: dict[str, Any]) -> None:
    """
    Increments and logs total number of orders created.
    :param data: event payload containing order details
    :return: nothing
    """
    global orders_count
    orders_count += 1
    print(f"[Analytics] Orders total: {orders_count}")

def log_order_paid(data: dict[str, Any]) -> None:
    """
    Increments and logs total number of processed payments.
    :param data: event payload containing payment details
    :return: nothing
    """
    global payments_count
    payments_count += 1
    print(f"[Analytics] Payments total: {payments_count}")