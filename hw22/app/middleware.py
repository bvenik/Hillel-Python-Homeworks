import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('app_custom_logger')

REQUEST_COUNT = 0


class CustomMetricsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        global REQUEST_COUNT
        REQUEST_COUNT += 1

        logger.info(f"МЕТРИКА: Запит №{REQUEST_COUNT} надіслано на URL: {request.path}")

    def process_response(self, request, response):
        response['X-Custom-Platform-Header'] = 'Django-Custom-Engine-V2'

        response['X-Total-Requests-Count'] = str(REQUEST_COUNT)

        return response
