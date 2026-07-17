from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from ..models import Server, MetricLog, Notification
from ..schemas import ServerIn, ServerOut, MetricLogIn, MetricLogOut, NotificationOut
from ..auth import bearer_auth

router = Router()


@router.get("/", response=List[ServerOut], auth=bearer_auth)
def list_servers(request):
    """
    Retrieves the list of servers registered under the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :return: list of Server instances
    """
    return Server.objects.filter(user=request.user)


@router.get("/{server_id}", response=ServerOut, auth=bearer_auth)
def get_server(request, server_id: int):
    """
    Retrieves a single server's details by its ID.
    :param request: standard Django HTTP request object containing authenticated user
    :param server_id: unique integer identifier of the server
    :return: Server instance or raises 404 Not Found
    """
    return get_object_or_404(Server, id=server_id, user=request.user)


@router.post("/", response={201: ServerOut}, auth=bearer_auth)
def create_server(request, data: ServerIn):
    """
    Registers a new server for monitoring.
    :param request: standard Django HTTP request object containing authenticated user
    :param data: Pydantic schema containing server name, IP address, and status
    :return: tuple of HTTP status code 201 and the created Server instance
    """
    server = Server.objects.create(
        user=request.user,
        name=data.name,
        ip_address=data.ip_address,
        is_online=data.is_online
    )
    return 201, server


@router.put("/{server_id}", response=ServerOut, auth=bearer_auth)
def update_server(request, server_id: int, data: ServerIn):
    """
    Updates the registered details of an existing server.
    :param request: standard Django HTTP request object containing authenticated user
    :param server_id: unique integer identifier of the server to update
    :param data: Pydantic schema containing updated server name, IP address, and status
    :return: updated Server instance
    """
    server = get_object_or_404(Server, id=server_id, user=request.user)
    server.name = data.name
    server.ip_address = data.ip_address
    server.is_online = data.is_online
    server.save()
    return server


@router.delete("/{server_id}", response={204: None}, auth=bearer_auth)
def delete_server(request, server_id: int):
    """
    Deletes a registered server.
    :param request: standard Django HTTP request object containing authenticated user
    :param server_id: unique integer identifier of the server to delete
    :return: tuple of HTTP status code 204 and None
    """
    server = get_object_or_404(Server, id=server_id, user=request.user)
    server.delete()
    return 204, None


@router.post("/{server_id}/metrics", response={201: MetricLogOut}, auth=bearer_auth)
def add_metrics(request, server_id: int, data: MetricLogIn):
    """
    Records new hardware metrics log for a server, triggering notifications if thresholds exceed 90%.
    :param request: standard Django HTTP request object containing authenticated user
    :param server_id: unique integer identifier of the server
    :param data: Pydantic schema containing CPU, Memory, and Disk usage percentages
    :return: tuple of HTTP status code 201 and the logged MetricLog instance
    """
    server = get_object_or_404(Server, id=server_id, user=request.user)

    metric_log = MetricLog.objects.create(
        server=server,
        cpu_load=data.cpu_load,
        memory_usage=data.memory_usage,
        disk_usage=data.disk_usage
    )

    threshold = 90.0
    alerts = []
    if data.cpu_load >= threshold:
        alerts.append(f"CPU Load critical: {data.cpu_load}%")
    if data.memory_usage >= threshold:
        alerts.append(f"Memory Usage critical: {data.memory_usage}%")
    if data.disk_usage >= threshold:
        alerts.append(f"Disk Usage critical: {data.disk_usage}%")

    for alert_msg in alerts:
        Notification.objects.create(
            server=server,
            message=alert_msg
        )

    return 201, metric_log


@router.get("/{server_id}/metrics", response=List[MetricLogOut], auth=bearer_auth)
def list_metrics(request, server_id: int):
    """
    Retrieves the historical metrics logs for a server, ordered from newest to oldest.
    :param request: standard Django HTTP request object containing authenticated user
    :param server_id: unique integer identifier of the server
    :return: list of MetricLog instances
    """
    server = get_object_or_404(Server, id=server_id, user=request.user)
    return MetricLog.objects.filter(server=server).order_by('-recorded_at')


@router.get("/{server_id}/notifications", response=List[NotificationOut], auth=bearer_auth)
def list_notifications(request, server_id: int):
    """
    Retrieves all generated notifications/alerts for a specific server.
    :param request: standard Django HTTP request object containing authenticated user
    :param server_id: unique integer identifier of the server
    :return: list of Notification instances
    """
    server = get_object_or_404(Server, id=server_id, user=request.user)
    return Notification.objects.filter(server=server).order_by('-created_at')


@router.put("/{server_id}/notifications/{notification_id}/read", response=NotificationOut, auth=bearer_auth)
def mark_notification_as_read(request, server_id: int, notification_id: int):
    """
    Marks a specific server alert notification as read.
    :param request: standard Django HTTP request object containing authenticated user
    :param server_id: unique integer identifier of the server
    :param notification_id: unique integer identifier of the notification
    :return: updated Notification instance
    """
    server = get_object_or_404(Server, id=server_id, user=request.user)
    notification = get_object_or_404(
        Notification, id=notification_id, server=server)
    notification.is_read = True
    notification.save()
    return notification
