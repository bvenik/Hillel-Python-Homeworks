import logging
from django.shortcuts import render

logger = logging.getLogger('django.security')


class SecurityLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ['/home/', '/admin/']

        if any(request.path.startswith(path) for path in protected_paths):
            user_id = request.session.get('user_id')
            username = request.session.get('username', 'Anonymous')
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown IP')

            if not user_id:
                logger.warning(
                    f"Unauthorized! Path: {request.path} | IP: {ip_address}"
                )
            else:

                logger.info(
                    f"User {username} (ID: {user_id}) visited {request.path} | IP: {ip_address}"
                )

        response = self.get_response(request)
        return response


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
