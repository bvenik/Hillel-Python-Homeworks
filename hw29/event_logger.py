from typing import Any

def log_user_deleted(data: dict[str, Any]) -> None:
    """
    Logs specific user deletion events to the console database log.
    :param data: event payload containing user details
    :return: nothing
    """
    print(f"[Logger] User removed from DB: {data}")

def log_all_user_events(data: dict[str, Any]) -> None:
    """
    Acts as a wildcard log catching all system events matching user namespace.
    :param data: event payload containing context details
    :return: nothing
    """
    print(f"[Logger] [Wildcard] User event system log: {data}")