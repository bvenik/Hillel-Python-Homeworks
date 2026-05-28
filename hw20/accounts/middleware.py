import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)


class AccessLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'protected' in request.path:
            user = request.user.username if request.user.is_authenticated else 'Anonymous'
            print(f"[SECURITY LOG] Access attempt to [{request.path}] by [{user}]")

        response = self.get_response(request)
        return response


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, 'accounts/404.html', status=404)
        return response

    def process_exception(self, request, exception):
        print(f"[CRITICAL ERROR] Server error: {exception}")
        return render(request, 'accounts/500.html', status=500)
