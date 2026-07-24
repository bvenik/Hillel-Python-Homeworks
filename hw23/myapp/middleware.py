from django.core.cache import cache
from django.http import HttpResponse


class AnonymousBooksCacheMiddleware:
    """
    Middleware that caches the books list page response for anonymous users.
    """

    def __init__(self, get_response) -> None:
        """
        Initializes the middleware.
        :param get_response: next middleware/view in the chain
        :return: nothing
        """
        self.get_response = get_response

    def __call__(self, request) -> HttpResponse:
        """
        Processes the request and caches the books list for anonymous users.
        :param request: HTTP request object
        :return: HTTP response object
        """
        if request.path == '/books/' and not request.user.is_authenticated:
            cache_key = 'anonymous_books_page'
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                cached_response['X-Middleware-Cache'] = 'HIT'
                return cached_response

            response = self.get_response(request)
            if request.method == 'GET' and response.status_code == 200:
                cache.set(cache_key, response, timeout=60)
                response['X-Middleware-Cache'] = 'MISS'
            return response

        return self.get_response(request)
