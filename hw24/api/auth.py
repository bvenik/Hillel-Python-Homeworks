from ninja.security import HttpBearer
from .models import APIToken


class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            api_token = APIToken.objects.get(token=token)
            request.user = api_token.user
            return api_token
        except APIToken.DoesNotExist:
            return None


bearer_auth = BearerAuth()
