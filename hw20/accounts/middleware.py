import logging
from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


class AccessLoggingMiddleware:
    """
    Middleware for logging access attempts to protected pages.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """
        Initialize the access logging middleware.

        :param get_response: A callable that takes a request and returns a response.
        :return: None
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the incoming HTTP request and log access to protected paths.

        :param request: The incoming HTTP request.
        :return: The generated HTTP response.
        """
        if 'protected' in request.path:
            user: str = request.user.username if request.user.is_authenticated else 'Anonymous'
            print(f"[SECURITY LOG] Access attempt to {request.path} by user: {user}")

        response: HttpResponse = self.get_response(request)
        return response


class ErrorHandlingMiddleware:
    """
    Middleware for handling 404 and 500 HTTP errors gracefully.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """
        Initialize the error handling middleware.

        :param get_response: A callable that takes a request and returns a response.
        :return: None
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the incoming HTTP request and intercept 404 Not Found responses.

        :param request: The incoming HTTP request.
        :return: The generated HTTP response or a custom 404 page.
        """
        response: HttpResponse = self.get_response(request)
        if response.status_code == 404:
            return render(request, 'accounts/404.html', status=404)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse:
        """
        Intercept critical server errors and render a custom 500 Internal Server Error page.

        :param request: The incoming HTTP request.
        :param exception: The exception raised during request processing.
        :return: A custom 500 HTTP response.
        """
        print(f"[CRITICAL ERROR] Server error occurred: {exception}")
        return render(request, 'accounts/500.html', status=500)
