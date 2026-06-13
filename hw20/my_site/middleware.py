import logging
from django.shortcuts import render

logger = logging.getLogger('django.security')


class SecurityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ['/home/', '/admin/']

        if request.path in protected_paths:
            if not request.session.get('user_id'):
                ip = request.META.get('REMOTE_ADDR')
                logger.warning(f"Unauthorized access attempt to {request.path} from IP {ip}")

        return self.get_response(request)


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return render(request, 'errors/404.html', status=404)

        if response.status_code == 500:
            return render(request, 'errors/500.html', status=500)

        return response
