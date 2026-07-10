from event_bus import EventBus

def create_order(bus: EventBus, order_id: int) -> None:
    """
    Simulates order creation and emits the corresponding event.
    :param bus: EventBus instance to emit the event through
    :param order_id: unique identifier of the order
    :return: nothing
    """
    print(f"\n[Orders] Creating order {order_id}...")
    bus.emit("order.created", {"order_id": order_id, "amount": 500})

def pay_order(bus: EventBus, order_id: int) -> None:
    """
    Simulates order payment and emits the corresponding event.
    :param bus: EventBus instance to emit the event through
    :param order_id: unique identifier of the order
    :return: nothing
    """
    print(f"\n[Orders] Order paying {order_id}...")
    bus.emit("order.paid", {"order_id": order_id, "amount": 500})