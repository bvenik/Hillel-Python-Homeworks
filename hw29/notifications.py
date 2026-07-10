from typing import Any

def send_email(data: dict[str, Any]) -> None:
    """
    Simulates sending an transactional email notice for an order.
    :param data: event payload containing order details
    :return: nothing
    """
    print(f"[Notifications] Sent email for order {data['order_id']}")

def send_sms(data: dict[str, Any]) -> None:
    """
    Simulates sending an SMS notice for a successful payment.
    :param data: event payload containing order details
    :return: nothing
    """
    print(f"[Notifications] Sent SMS with success payment {data['order_id']}")

def send_welcome_email(data: dict[str, Any]) -> None:
    """
    Simulates sending a welcome email to a new user.
    :param data: event payload containing user details
    :return: nothing
    """
    print(f"[Notifications] Sent 'welcome' email to user {data['user_id']}")