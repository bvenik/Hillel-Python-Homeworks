from event_bus import EventBus
import orders
import notifications
import analytics
import event_logger

if __name__ == "__main__":
    bus: EventBus = EventBus()

    bus.subscribe("user.registered", notifications.send_welcome_email)
    bus.subscribe("user.deleted", event_logger.log_user_deleted)
    bus.subscribe("order.created", analytics.log_order_created)
    bus.subscribe("order.created", notifications.send_email)
    bus.subscribe("user.*", event_logger.log_all_user_events)
    bus.subscribe("order.paid", notifications.send_sms)
    bus.subscribe("order.paid", analytics.log_order_paid)

    bus.emit("user.registered", {"user_id": 1, "name": "Test name"})
    bus.emit("user.deleted", {"user_id": 2})

    orders.create_order(bus, 1)
    orders.pay_order(bus, 1)

    bus.subscribe("order.paid", notifications.send_email)
    bus.unsubscribe("order.paid", notifications.send_email)
    orders.pay_order(bus, 999)

    bus.event_queue.join()

    print("\nEvent log")
    for log in bus.event_log:
        print(log)
