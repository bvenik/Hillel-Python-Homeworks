from ninja import Router
from typing import List, Optional
from django.shortcuts import get_object_or_404
from ..models import Task
from ..schemas import TaskIn, TaskOut
from ..auth import bearer_auth

router = Router()


@router.get("/", response=List[TaskOut], auth=bearer_auth)
def list_tasks(
    request,
    is_completed: Optional[bool] = None,
    sort_by: Optional[str] = None
):
    """
    Retrieves the list of tasks for the authenticated user with optional filtering and sorting.
    :param request: standard Django HTTP request object containing authenticated user
    :param is_completed: optional boolean filter for task completion status
    :param sort_by: optional string sorting parameter ('created_at', '-created_at', 'due_date', '-due_date')
    :return: list of tasks matching the criteria
    """
    tasks = Task.objects.filter(user=request.user)

    if is_completed is not None:
        tasks = tasks.filter(is_completed=is_completed)

    if sort_by == "created_at":
        tasks = tasks.order_by("created_at")
    elif sort_by == "-created_at":
        tasks = tasks.order_by("-created_at")
    elif sort_by == "due_date":
        tasks = tasks.order_by("due_date")
    elif sort_by == "-due_date":
        tasks = tasks.order_by("-due_date")

    return tasks


@router.get("/{task_id}", response=TaskOut, auth=bearer_auth)
def get_task(request, task_id: int):
    """
    Retrieves a single task by its ID for the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :param task_id: unique integer identifier of the task
    :return: Task instance or raises 404 Not Found
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return task


@router.post("/", response={201: TaskOut}, auth=bearer_auth)
def create_task(request, data: TaskIn):
    """
    Creates a new task for the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :param data: Pydantic schema containing task title, description, status, and due date
    :return: tuple of HTTP status code 201 and the created Task instance
    """
    task = Task.objects.create(
        user=request.user,
        title=data.title,
        description=data.description,
        is_completed=data.is_completed,
        due_date=data.due_date
    )
    return 201, task


@router.put("/{task_id}", response=TaskOut, auth=bearer_auth)
def update_task(request, task_id: int, data: TaskIn):
    """
    Updates an existing task for the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :param task_id: unique integer identifier of the task to update
    :param data: Pydantic schema containing updated task title, description, status, and due date
    :return: updated Task instance
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.title = data.title
    task.description = data.description
    task.is_completed = data.is_completed
    task.due_date = data.due_date
    task.save()
    return task


@router.delete("/{task_id}", response={204: None}, auth=bearer_auth)
def delete_task(request, task_id: int):
    """
    Deletes an existing task for the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :param task_id: unique integer identifier of the task to delete
    :return: tuple of HTTP status code 204 and None
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return 204, None
